object Form2: TForm2
  Left = 0
  Top = 0
  Caption = 'Open Files'
  ClientHeight = 288
  ClientWidth = 457
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  OnCreate = Form2Create
  PixelsPerInch = 96
  TextHeight = 13
  object Button1: TButton
    Left = 168
    Top = 240
    Width = 88
    Height = 32
    Caption = 'Open'
    TabOrder = 0
    OnClick = Button1Click
  end
  object Memo1: TMemo
    Left = 0
    Top = 0
    Width = 456
    Height = 216
    Lines.Strings = (
      '')
    TabOrder = 1
  end
end
