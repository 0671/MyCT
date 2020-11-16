# coding:utf-8
import random
import dns.resolver

class domainClass(object):
    def __init__(self,priority,domain):
        self.priority = priority
        self.domain = domain
    
    def __lt__(self,other): 
        return self.priority < other.priority
                   
    def __str__(self):
        return self.domain


class c2Class(object):
	def __init__(self):
		self.name=' lijiejie/subDomainsBrute'
		self.description='A fast sub domain brute tool for pentesters'
		self.refer='https://github.com/lijiejie/subDomainsBrute'
		
		self.rootdomain = None
		self.nextsubs = set()
		self.next_sub_file='data\\next_sub.txt' # 通配符{next_sub}对应的子域集合
		self.subs_file='data\\subnames.txt' # 爆破使用的子域集合

		with open(self.next_sub_file) as f:
			for i in f:
				i = i.strip()
				self.nextsubs.add(i)
		self.regex_list = {
		'{next_sub}':self.nextsubs,
		'{alphnum}':'abcdefghijklmnopqrstuvwxyz0123456789',
		'{alpha}':'abcdefghijklmnopqrstuvwxyz',
		'{num}':'0123456789'}
		self.subs = set()
		with open('data\\subnames.txt') as f:
			for i in f:
				i = i.strip()
				self.subs.add(i)
		self.depth = 1 # 检测深度,默认向下检测1级域名
		self.startlevel = 0
		self.timeout_comain = {}
		self.dns_servers = []
		# dns解析器集生成
		from gevent.pool import Pool
		pool = Pool(6)
		for s in ['119.29.29.29','182.254.116.116','114.114.115.115','114.114.114.114','223.5.5.5','223.6.6.6']:
			pool.apply_async(self.test_server, (s, self.dns_servers))
		pool.join()
		self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(100)]
		for r in self.resolvers:
			r.lifetime = 4
			r.timeout = 10.0
			i1 = random.choice(range(len(self.dns_servers)))
			i2 = (i1+1)%len(self.dns_servers)
			r.nameservers = [self.dns_servers[i1],self.dns_servers[i2]]
		self.find_subdomains=set()


	def c2Func(self,target):
		# 选择dns解析器
		resolver = random.choice(self.resolvers)
		cdomain = str(target)
		# 设置根域
		if self.rootdomain == None: 
			self.rootdomain = cdomain
			self.startlevel = cdomain.count('.')
		# 如果当前域名级别比查询最高级还高，直接退出、
		if cdomain.count('.') > self.startlevel+self.depth:
			return 0,''
		# 根域需要子域赋值
		if self.rootdomain == cdomain:
			keepcheck = self.sdbGenerate(cdomain)
			return -1,keepcheck
		# 替换占位符
		for r in self.regex_list:
			if r in cdomain:
				keepcheck=[]
				for i in self.regex_list[r]:
					keepcheck.append(domainClass(cdomain.count('.'),cdomain.replace(r,i,1)))
				return -1,keepcheck
		# 进行查询
		try:
			answers = resolver.query(cdomain)
			if answers:# 查询成功
				if cdomain in self.find_subdomains:
					raise Exception('Repeat domain') # 如果存在则报异常
				self.find_subdomains.add(cdomain)
				ips = ', '.join(sorted([answer.address for answer in answers]))
				# info = cdomain + '->' + ips
				info = [cdomain]
				if cdomain.count('.') == self.startlevel+self.depth: #达到深度
					# return 1,cdomain+'->'+ips # 直接返回
					return 1,cdomain # 直接返回
				keepbrute = []
				try: # 查询cname
					answers =  resolver.query(cdomain,'cname')
					cname = answers[0].target.to_unicode().rstrip('.')
					if cname.endswith(self.rootdomain) and cname not in self.find_subdomains: # 根域之下且不是已发现的域名
						self.find_subdomains.add(cname)
						info.append(cname)
						keepbrute.append(domainClass(cname.count('.'),cname))
				except Exception as e:
					pass
				# 下一个深度的子域赋值
				keepbrute.extend(self.sdbGenerate(cdomain))
				return 10,(info,keepbrute)
		except dns.resolver.NoNameservers as e: # ns不可访问
			return -1,domainClass(cdomain.count('.'),cdomain)
		except dns.exception.Timeout as e:# 查询延时
			self.timeout_comain[cdomain] = self.timeout_comain.get(cdomain, 0) + 1
			if self.timeout_comain[cdomain] <=1:
				return -1,domainClass(cdomain.count('.'),cdomain)
		except (dns.resolver.NoAnswer,dns.resolver.NXDOMAIN) as e: # 查询不到域名
			pass
		except dns.name.EmptyLabel as e:
			pass
		except Exception as e:
			# print(e)
			pass
		return 0,''

	# 可信dns服务器检测
	def test_server(self,server,dns_servers):
		resolver = dns.resolver.Resolver(configure=False)
		resolver.lifetime = resolver.timeout = 5.0
		resolver.nameservers = [server]
		try:
			answers = resolver.query('public-dns-a.baidu.com')
			if answers[0].address != '180.76.76.76':
				raise Exception('Incorrect DNS response')
			try:
				resolver.query('false.domain.123.123.baidu.com')
			except Exception as e:
				dns_servers.append(server)
		except Exception as e:
			pass
	# 子域集生成
	def sdbGenerate(self,rdomain):
			keepbrute=[]
			for s in self.subs:
				keepbrute.append(domainClass(rdomain.count('.')+1,s+'.'+rdomain))
			return keepbrute


if __name__ == '__main__':
	target="gzport.com"
	pocObj=c2Class()
	print(pocObj.c2Func(target))