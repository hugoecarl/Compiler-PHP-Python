<?php  

function fdsf($x) {
    if ($x == 0){
    return 1;
    } else {
    $y = fdsf($x - 1) + 3;
    return $y;
    }
}

function sf($x, $y) {
    return $x - $y;
    echo 3;
    return $x + $y;
}


function sos($d) {
    if ($d > 1) {
        sos($d - 1);
    }
    echo $d;
}


sos(4);

echo sf(3, 2);


?>