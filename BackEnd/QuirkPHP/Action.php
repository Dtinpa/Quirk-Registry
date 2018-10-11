<?php
//Dana Thompson
//dtdthomp54@gmail.com

//This file facilitates retrieving actions from the db
require_once 'DBShared.php';
require_once 'DBConn.php';

class Action extends DBShared  {
	function __construct() {
        $this->tableName = "BodyAction";
    }
}
?>