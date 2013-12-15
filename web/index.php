<!doctype html>
<html>
<head>
<title>
Horoscope Generator | Statistically Insignificant Wisdom
</title>
<style>
html {
	min-width: 100%;
	min-height: 100%;
	background-image: url('bg.jpg');
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}
body {
	background-color: rgba(50, 50, 50, .6);
	width: 70%;
	margin: 5% auto;
	padding: 20px;
	padding-top: 100px;
	padding-bottom: 100px;
	border-radius: 10px;
	text-align: center;
	font-family: arial;
	color: white;
}
</style>
</head>
<body>
<h1><?php echo exec('python horoscope.py'); ?></h1>
</body>
</html>
