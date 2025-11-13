insert into attacks_attack_payload (payload_id, attack_id, payload, order_by, description) 

SELECT	attacks_payload.payload_id,
		attack.attack_id, 
		payload_default, 
		ifnull(max_order_by,0)+1 as max_order_by, 
		'Default Payload' as description

FROM	attacks_attack attack

		left outer join (select attack_id, max(order_by) max_order_by from attacks_attack_payload group by attack_id) as payload_max_order_by 
			on payload_max_order_by.attack_id = attack.attack_id 		
	
		left outer join attacks_payload 
			on attacks_payload.payload = payload_default 
			
WHERE	attack.payload_default is not null and 
		attack.attack_id not in ( 
			select	attack_id 
			from 	attacks_attack_payload ap
			WHERE	ap.attack_id = attack.attack_id and 
					ap.payload = attack.payload_default
		)   
;


update 	session_required = 'no';
from 	attacks_attack;

update  session_required = 'yes' 
FROM	attacks_attack a
where 	a.attack_id in ( 
		SELECT	distinct attack.attack_id 
		FROM	attacks_attack as attack
				left outer join attacks_option_heading as oh
					on oh.attack_id = attack.attack_id 
				join attacks_option as o 
					on o.option_heading_id = oh.option_heading_id and 
						o.name = 'SESSION' 
		);