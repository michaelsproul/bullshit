<?php 
header('Content-Type: application/json');
$data = array();
$data['result'] = exec('python horoscope.py');
echo json_encode($data);
?>
