<?php
error_reporting(0);
class Good{
    public $g1;
    private $gg2;

    public function __construct($ggg3)
    {
        $this->gg2 = $ggg3;
    }

    public function __isset($arg1)
    {
        if(!preg_match("/a-zA-Z0-9~-=!\^\+\(\)/",$this->gg2))
        {
            if ($this->gg2)
            {
                $this->g1->g1=666;
            }
        }else{
            die("No");
        }
    }
}
class Luck{
    public $l1;
    public $ll2;
    private $md5;
    public $lll3;
    public function __construct($a)
    {
        $this->md5 = $a;
    }
    public function __toString()
    {
        $new = $this->l1;
        return $new();
    }

    public function __get($arg1)
    {
        $this->ll2->ll2('b2');
    }

    public function __unset($arg1)
    {
        if(md5(md5($this->md5)) == 666)
        {
            if(empty($this->lll3->lll3)){
                echo "There is noting";
            }
        }
    }
}

class To{
    public $t1;
    public $tt2;
    public $arg1;
    public function  __call($arg1,$arg2)
    {
        if(urldecode($this->arg1)===base64_decode($this->arg1))
        {
            echo $this->t1;
        }
    }
    public function __set($arg1,$arg2)
    {
        if($this->tt2->tt2)
        {
            echo "what are you doing?";
        }
    }
}
class You{
    public $y1;
    public function __wakeup()
    {
        unset($this->y1->y1);
    }
}
class Flag{
    public function __invoke()
    {
        echo "May be you can get what you want here";
        array_walk($this, function ($make, $colo) {
            $three = new $colo($make);
            foreach($three as $tmp){
            echo ($tmp.'<br>');
            }  
        });
    }
}

if(isset($_POST['D0g3']))
{
    unserialize($_POST['D0g3']);
}else{
    highlight_file(__FILE__);
}
?>
