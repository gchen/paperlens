<?php
require_once("../../db.php");

function GetRelatedItems($item, $topN)
{
	$ret = array();
	$result = mysql_query('select author_id,rank from paper_author where paper_id='. $item . '  order by rank limit 3');
	if (!$result) {
	    die('Query failed: ' . mysql_error());
	}

	while ($row = mysql_fetch_row($result))
	{
		$author_id = $row[0];
		$rank = $row[1];
		if($rank == 0) $rank_query = ' and rank == 0';
		else $rank_query = ' and rank > 0';
		$rel_results = mysql_query('select paper_id from paper_author where author_id='.$author_id . ' ' . $rank_query);
		if(!$rel_results) continue;
		while($rel_row = mysql_fetch_row($rel_results))
		{
			$rel_paper_id = $rel_row[0];
			if($rel_paper_id != $item)
			{
				if(!array_key_exists($rel_paper_id, $ret))
					$ret[$rel_paper_id] = 0;
				$ret[$rel_paper_id]++;
			}
		}
	}
	arsort($ret);
	return array_slice($ret, 0, $topN, TRUE);
}

$id = $_GET['id'];
$related_items = GetRelatedItems($id, 10);
header('Content-Type: text/xml');
echo '<relate>';
foreach($related_items as $id => $weight)
{
	//echo $id . ',' . $weight . '    ';
	echo file_get_contents('http://127.0.0.1/api/paper.php?id=' . $id) ;
}
echo '</relate>';
?>