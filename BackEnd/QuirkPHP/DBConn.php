<?php
require_once('../../QuirkPHP/config.php');

//Only serves to facilitate DB connections.
function OpenCon() {
	$conn = new mysqli(DBHOST, DBUSER, DBPASS, DBNAME) or die("Connection failed");


	return $conn;
}
 
function CloseCon($conn) {
	$conn -> close();
}
   
?>
