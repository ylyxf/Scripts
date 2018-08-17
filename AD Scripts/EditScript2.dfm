object Form2: TForm2
  Left = 182
  Top = 161
  Caption = 'Hello World'
  ClientHeight = 472
  ClientWidth = 567
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 112
    Top = 120
    Width = 25
    Height = 13
    Caption = 'Label'
    Color = clHighlight
    ParentColor = False
  end
  object bDisplay: TButton
    Left = 224
    Top = 264
    Width = 75
    Height = 25
    Caption = 'Display'
    TabOrder = 0
    OnClick = bDisplayClick
  end
  object bClose: TButton
    Left = 344
    Top = 264
    Width = 75
    Height = 25
    Caption = 'Close'
    TabOrder = 1
    OnClick = bCloseClick
  end
end
