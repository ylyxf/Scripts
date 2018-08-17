object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 368
  ClientWidth = 595
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  OnCreate = Form1Create
  PixelsPerInch = 96
  TextHeight = 13
  object TMemo1: TMemo
    Left = 48
    Top = 24
    Width = 488
    Height = 200
    Lines.Strings = (
      'TMemo1')
    TabOrder = 0
    WordWrap = False
  end
  object Button1: TButton
    Left = 184
    Top = 256
    Width = 200
    Height = 56
    Caption = 'Change Description'
    TabOrder = 1
    OnClick = Button1Click
  end
end
