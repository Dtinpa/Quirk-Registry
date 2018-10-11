<?php
//Dana Thompson
//dtdthomp54@gmail.com

//This file facilitates retrieving actions from the db.
include 'DBConn.php';
// Dana Thompson
// dtdthomp54@gmail.com

//This is an abstract class that holds shared queries between different tables
abstract class DBShared {
	protected $tableName;
	
	// Retrieves a random entry from any of the rows from a specified column
	public function getRandomRow($colName) {
		$conn = OpenCon();

		// Most likely redundant since only I can change the values of these variables,
		// But this just sanitizes them a bit just in case.
		$colN = mysqli_real_escape_string($conn, $colName);
		$tableN = mysqli_real_escape_string($conn, $this->tableName);
		
		$sql = "SELECT $colN FROM $tableN ORDER BY RAND() LIMIT 1;";
		$result = $conn->query($sql);
		$randRow = "";

		// Retrieve the result of the query
		if ($result->num_rows > 0) {
			while($row = $result->fetch_assoc()) {
				$randRow = $row[$colName];
			}
		}
 
		CloseCon($conn);
		return $randRow;
	}
}
?>