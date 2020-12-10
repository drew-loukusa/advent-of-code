# Create Folder and blank python script for day N
for($n=4; $n -le 25; $n +=1 ){
   $day_template = Get-Content .\day_template.txt
   $day_template = $day_template -Replace "{DAYREPLACE}",$n 
    
   Set-Content -Path "day$n\day$n.py"  -Value $day_template
}
