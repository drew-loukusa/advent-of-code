$YEAR=2021
mkdir "$YEAR"
Set-Location $YEAR

# Create Folder and blank python script for day N
for($DAY=3; $DAY -le 25; $DAY +=1 ){
   $dirpath = "day$DAY"
   if ($DAY -lt 10){
      $dirpath = "day0$DAY"
   }

   mkdir $dirpath

   $part_template = Get-Content ..\part_template.txt
   $part_template = $part_template -Replace "{DAY_REPLACE}", $DAY
   $part_template = $part_template -Replace "{YEAR_REPLACE}", $YEAR
   $part_template = $part_template -Replace "{PART_REPLACE}", 'a'   
   Set-Content -Path "$dirpath\part_a.py"  -Value $part_template
   
   $part_template = Get-Content ..\part_template.txt
   $part_template = $part_template -Replace "{DAY_REPLACE}", $DAY
   $part_template = $part_template -Replace "{YEAR_REPLACE}", $YEAR
   $part_template = $part_template -Replace "{PART_REPLACE}", 'b'
   Set-Content -Path "$dirpath\part_b.py"  -Value $part_template
}
Set-Location ..
