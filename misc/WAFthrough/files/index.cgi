#!/bin/bash
 
exec 2>&1 # for debug

SECCON_BANNER="iVBORw0KGgoAAAANSUhEUgAAAT8AAABACAYAAABspXALAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAGKUlEQVR4nO3dT2gUVxwH8N+b2ZndmB3bGLcWo1gtPbQRabuHIAYhJUIVERSSg4f6h8Sc7EUvhVihCl576cFEMIp4iOhJSKGsQolED0uhuIKl2a3aQnXNn7puJpk3M6+XJphkNzWT2dmdvO8HAsu+eTO/x85+mbdvdkMEAAAAAHJgSzzPOjo6GBFRPp9nhUKh3LYAADXFMAyRSCQEEdGNGzcEEc3+zSkVaIyImOM43wshPp3dRgiB8AOAUGCMCdu2f21razttWZadTqcdWhCAkVL9ksmkKoT4TFXV1sCqBQDwkeM4KhHVNXI+k0wmrTcCkIiIlIUdOjo6mK7rEVzpAUCYcc41xphRqK+P6roemf0Yb9ai8CMiikajquu6JdsAAMLAcRyVcR6PWFY0Go2qC9sXTXvz+TwzTVOhBZ8HvujZXcEyg3F3y85/7uTG36l2HQBQGRf7++ceu66rOqoaJd3VLNNU8vn8vExbFH7/reoy13XnbcgHM5WqNzC/74/bfdeGql0GAFTIgvBTIkSa7WiKbfNFd6yUnNoahoPP+wAg9IQQTHddVirTSq32/i+ts5liLbtWXlkAioO3yH3wsmTb5YGBYIvx6M9nz+jMmTMl2050ddHO1nAsyl+/eoV+unO3ZNu5c+do0+bNAVfkzbGjR8u2rYZzas8XbXT4qyMBV+TNyPAw9V265Kmvp/CLteyitccveDpg0KYf3CsbfkePhOMFzmQelT1Rd7a2hmYcI8PDRGXC7+DBQ9Tc/EnAFXmzVPiF5bVY6pzauu3D0IyDiDyHH1Z0AUBKCD8AkBLCDwCkhPADACl5WvAoR0xNEh9N+7nLFROTr5fd548nT6j4uliBarx5/NtjT/0ymUc+V7IykxMTy+4zZZqUy+YqUE2wXo6N0fO/nwd+3A3vb6D1jY2+7a9a742t27bSmro6X/fpa/jx0TTld3f6ucuquHD+vOcVpFqyfXtztUtYsVw2tyrGcfv27SVXiSvl8sCAryu31XpvPHyY8f1uAEx7AUBKCD8AkBLCDwCkhPADACkh/ABASgg/AJASwg8ApITwAwApIfwAQEoIPwCQkq9fb1PqG0jrrK2vIvH7WaKn5rL6NO/YQSe6uipU0fJNTkzQ4M2b1S4DYFXxNfwi2z6n9y7+7OcuV+xFz27iT5f3z5e+PnmyQtV4k8k8QvgB+AzTXgCQEsIPAKSE8AMAKSH8AEBKCD8AkJKn1d7CqT4qnOrzuxbPtM5mX1eZe7q7V8UvOQNAebjyAwApIfwAQEoIPwCQEsIPAKSE8AMAKSH8AEBKCD8AkBLCDwCkhPADACkh/ABASp6+3qa0rCd1ywa/a/FM/3i7r/tbLb/kXEtjICJKpVI0msstq099vL7mxuHlq49NTU1VGUdTU1PgxwwLT+FX33mI1h6/4HctNWO1/JLzxf7+ClTjXU93N40uMzg+2LKl5sbhJfz2tLfTnvb2ClQDXmHaCwBSQvgBgJQQfgAgJYQfAEgJ4QcAUvK02lscvEXTD+75XUtF8PvZsm093d0BVuLd5MRE2bbrV6/QyPBwgNV4l0qlyrZ9d/ZberehIcBqKmM1nFOpVKrsOJZ6DSup3PmRy4563idb+EQymdQMw6kfGhr5MRaLtcw+/1dDo+eD1IqB/S1jvdeGwj8QAChJCDH3eHx8/OGBffu6VSGeK2usiUJBLabTaT7bjmkvAEjprae9+g+nxypZSBC+XPuB+9GBY6EfBwCU9dYzu7cOv8Thb0I/XUwQUbLaRQBATcC0FwCktCj8DMMQhYIqSm0MABAWjDEhVNexIxG3UFCFYRjzcq3ktDcWi7kjIyNnOZ/Z9OrVa2NmairGbVsTjDH25nIKAEANmc0oLRLhxWLxpWIzizPHicVi7sJtF4VfIpEQ2WzW6e3t/UWx7RwxZgiiOiLShBCLbo0BAKgljDFBRJwRmURkqqpqTU9POxs3bpx34VYqzJS9e/dq4+PjUdd119QxVudork4W83RDNABA4HRhq1yxTCFMRVGm1q1bNzM0NMSJaO4KsFSgiXg8bpumyTjngruuFVGiqqVYWBwBgFDQFd3lqu3oisI1TePxeNwmonlXfv8CPZ0CMRn0ffwAAAAASUVORK5CYII="

echo "Content-Type: text/html"
echo ""

cat << SECCON
<!doctype html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<title>S E C C O N champions</title>
</head>
<body>

<div class="container-fluid">
  <div class="row">
    <div class="ml-2">
      <h1><img src="data:image/png;base64,$SECCON_BANNER" /> champions</h1>
    </div>
  </div>
</div>

<form name="t" class="form-inline" action="$SCRIPT_NAME" method="get" enctype="application/x-www-form-urlencoded">
  <div class="container-fluid">
    <div class="row">
      <div class="ml-3">
	<input class="form-control" name="q" type="radio" value="v" onclick="document.t.submit()" >2015
        <input class="form-control" name="q" type="radio" value="w" onclick="document.t.submit()" >2016
        <input class="form-control" name="q" type="radio" value="x" onclick="document.t.submit()" >2017
        <input class="form-control" name="q" type="radio" value="y" onclick="document.t.submit()" >2018
        <input class="form-control" name="q" type="radio" value="z" onclick="document.t.submit()" >2019
      </div>
    </div>
  </div>
</form>

<div class="container-fluid">
  <div class="row">
    <div class="ml-3">
      <h2>
SECCON

if [ "$REQUEST_METHOD" = "GET" ]
then
  VAR="$(echo $QUERY_STRING|cut -c3-|nkf -w --url-input)"
  TARGET_FILE=$(sed -e 's/z/2019/g' -e 's/y/2018/g' -e 's/x/2017/g' -e 's/w/2016/g' -e 's/v/2015/g' <(echo $VAR))
  if [[ "$TARGET_FILE" -gt 2014 ]]
  then
    echo '<HR>'
    cat $TARGET_FILE
  fi
fi

cat << SECCON
      </h2>
    </div>
  </div>
</div>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
SECCON


