<?php
highlight_file(__file__);
$d0g3=$_GET['d0g3'];
$name=$_GET['name'];
if(preg_match('/^(?:.{5})*include/',$d0g3)){
	$sorter='strnatcasecmp';
	$miao = create_function('$a,$b', 'return "ln($a) + ln($b) = " . log($a * $b);');
	if(strlen($d0g3)==substr($miao, -2)&&$name===$miao){
		$sort_function = ' return 1 * ' . $sorter . '($a["' . $d0g3 . '"], $b["' . $d0g3 . '"]);';
		@$miao=create_function('$a, $b', $sort_function);
	}
	else{
		echo('Is That My Name?');
	}
}
else{
	echo("YOU Do Not Know What is My Name!");
}
?>