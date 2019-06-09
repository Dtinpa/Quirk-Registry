<?php
// Dana Thompson
// dtdthomp54@gmail.com

// This file is responsible for accumulating all the data needed to make the quirk
// then sending it back to the client for final construction

require_once '../../QuirkPHP/Action.php';
require_once '../../QuirkPHP/Activity.php';

session_start();

$min_time = 30;
$max_requests = 7;

//the token sent must match the token from the page, to verify that a session from the start page was setup.
//This is used to block nefarious bots from spamming my spiders.
//Any user wishing to get my data must comply with these parameters, assuming they use the same cookie
//We don't need to worry about session high-jacking either since there are no user accounts
if(isset($_GET['token']) && strcmp(bin2hex($_GET['token']), $_SESSION['token'])) {
	if(!isset($_SESSION['visitCount'])) {
		$_SESSION['visitCount'] = 0;
	}
	
	//if its not already set, then set the requests 
	if(!isset($_SESSION['requests'])) {
		$_SESSION['requests'] = ['time' => time()];
	} else {
		$_SESSION['requests'][] = ['time' => time()];
	}
	$requests = $_SESSION['requests'];
	
	//For each past request, check if its been within the past 30 seconds, and mark them
	//If they're older than 30 seconds, then get rid of them, they're no longer needed
	$recentRequests = 0;
	foreach($requests as $index => $request) {
		if($request['time'] >= time() - $min_time) {
			$recentRequests++;
		} else {
			unset($_SESSION['requests'][$index]);
		}
	}
	
	//if more than the max requests are made in a set time span, then refuse the request
	if($max_requests <= $recentRequests) {
		echo json_encode(array("error" => "Connection refused"));
		exit(0);
	}
	
	// This works because the ".." is one of the hidden directories that contains
	// a reference to the parent directory.
	$path = realpath(dirname(__FILE__) . '/..');
	$output = shell_exec('sh ' . $path . '/executePython');

	$action = new Action();
	$activity = new Activity();

	// splits the json string output into an array so they can be inserted
	// individually
	$splitOutput = explode("\n", trim($output));

	$result = array("action" => $action->getRandomRow("action"),
					"activity" => $activity->getRandomRow("activity"));
					
	// Loop through output and merge it with the existing result Array/Object
	// There won't be duplicate key values, and sort order doesn't matter
	foreach($splitOutput as $attr) {
		$decoded = json_decode($attr,true);
		$result = array_merge($result, $decoded);
	}
					
	echo json_encode($result);
}
?>