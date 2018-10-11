<?php
//Dana Thompson
//dtdthomp54@gmail.com

//This file facilitates retrieving acctivities from the db
require_once 'DBShared.php';
require_once 'DBConn.php';

class Activity extends DBShared  {
	function __construct() {
        $this->tableName = "Activity";
    }
}
?>