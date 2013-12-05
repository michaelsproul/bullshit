<style>
html, body {
	padding: 0;
	margin: 0;
}
html {
	min-width: 100%;
	min-height: 100%;
	background-image: url('bg.jpg');
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}
body {
	width: 70%;
	font-family: arial;
	color: white;
	background-color: rgba(50, 50, 50, .6);
	margin: 5% auto;
	padding: 20px;
	padding-top: 100px;
	padding-bottom: 100px;
	border-radius: 10px;
	text-align: center;
}
</style>

<h1><?php echo exec('python horoscope.py'); ?></h1>
