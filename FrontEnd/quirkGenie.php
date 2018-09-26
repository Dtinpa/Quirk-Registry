<?php
// Dana Thompson
// dtdthomp54@gmail.com

// This file is responsible for accumulating all the data needed to make the quirk
// then sending it back to the client for final construction

require_once '../../QuirkPHP/Action.php';
require_once '../../QuirkPHP/Activity.php';

// This works because the ".." is one of the hidden directories that contains
// a reference to the parent directory.
$path = realpath(dirname(__FILE__) . '/..');
$output = shell_exec('sh ' . $path . '/executePython');

$action = new Action();
$activity = new Activity();

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
?>