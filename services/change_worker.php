<?php
$url = "http://aires.astoria-tula.ru/sharedapi/worker/update";

$apikey = $argv[1];  // Первый параметр
$user_id = $argv[2];    // Второй параметр
$value_field = $argv[3];    // Второй параметр

$params = array(
    array(
        'id' => $user_id,
        'fields' => array(
            array('id' => 3657, 'value' => $value_field),
        )
    )
);

$post = array(
    'apikey' => "$apikey",
    'params' => $params
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$result = json_decode(curl_exec($ch), true);
curl_close($ch);
print_r($result);
return $result;
?>