$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$publicDir=Join-Path (Split-Path $PSScriptRoot -Parent) 'public'
foreach($size in @(16,32,80)) {
  $bitmap=[Drawing.Bitmap]::new($size,$size)
  $graphics=[Drawing.Graphics]::FromImage($bitmap)
  $graphics.Clear([Drawing.ColorTranslator]::FromHtml('#175d54'))
  $font=[Drawing.Font]::new('Georgia',[single]($size*0.65),[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $format=[Drawing.StringFormat]::new()
  $format.Alignment=[Drawing.StringAlignment]::Center
  $format.LineAlignment=[Drawing.StringAlignment]::Center
  $graphics.DrawString('T',$font,[Drawing.Brushes]::White,[Drawing.RectangleF]::new(0,0,$size,$size),$format)
  $bitmap.Save((Join-Path $publicDir "icon-$size.png"),[Drawing.Imaging.ImageFormat]::Png)
  $format.Dispose(); $font.Dispose(); $graphics.Dispose(); $bitmap.Dispose()
}
