<?php

function recommendationCore($features, $table_name, $topN)
{
	$ret = array();
	foreach($features as $item=>$preference)
	{
		$related_items = GetRelatedItems($item, $table_name, $topN);
		foreach($related_items as $related_item=>$similarity)
		{
			if(!array_key_exists($related_item, $ret))
			{
				$ret[$related_item] = 0;
			}
			$ret[$related_item] += $preference * $similarity;
		}
	}
	return $ret;
}

?>