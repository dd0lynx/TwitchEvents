Clear-Host

$env:FLASK_APP="twitcheventsbot"
$env:FLASK_ENV="development"

python -m flask run --host=0.0.0.0