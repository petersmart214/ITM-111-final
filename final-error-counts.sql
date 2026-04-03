use ev_charger;
SELECT 
    GROUP_CONCAT(
		concat(
			'sum(`', flag_name, '`) as `', flag_name, '_count`'
        )
    ) INTO @col_names
FROM error_flag;

SELECT 
    GROUP_CONCAT(
        CONCAT(
            '(session.error_flag & ',
            bit_mask,
            ') != 0 AS `',
            flag_name, '`'
        )
    ) INTO @cols
FROM error_flag;

set @to_exec = concat(
	'select ',
    @col_names,
    ' from ',
	'(select ',
    @cols,
    ' from `session`) as c'
);

PREPARE stmt FROM @to_exec;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;