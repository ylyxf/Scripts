using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;
using Altium.Sdk.DxpAppServer;

namespace ConsoleApplication1
{
    class Vault
    {
        static void Main(string[] args)
        {
            List<string> pythonScripts = dirPyFiles();
            if (pythonScripts != null)
            {
                int fileIndex = 1;
                
                foreach (string fileName in pythonScripts)
                { 
                    Console.WriteLine("[" + fileIndex + "] " + fileName.Replace("Python Scripts\\", ""));
                    fileIndex += 1;
                }

                Console.WriteLine("Choose a script to execute");
                string inputIndex = Console.ReadLine();
                fileIndex = 0;
                int.TryParse(inputIndex, out fileIndex);
                while (fileIndex == 0 || fileIndex > pythonScripts.Count)
                {
                    Console.WriteLine("Input the index of file");
                    inputIndex = Console.ReadLine();
                    int.TryParse(inputIndex, out fileIndex);
                }

                string scriptName = pythonScripts[fileIndex - 1];
                runScript(scriptName);    
            }
            
        }

        static private List<string> dirPyFiles()
        {
            List<string> fileList = new List<string>();
            List<string> notFile = new List<string>()
            { 
                "Python Scripts\\cmpLib_advanced_ipy.py",
                "Python Scripts\\cmpLib_ipy.py"
            };

            string[] pyFiles = Directory.GetFiles("Python Scripts", "*.py");
            foreach (string fileName in pyFiles)
            {
               if (notFile.Contains(fileName) == false)
               {
                   fileList.Add(fileName);
               }
            }

            return fileList;

        }

        static private void runScript(string scriptFile)
        {
            ScriptEngine engine = Python.CreateEngine();
            ScriptScope scope = engine.CreateScope();
            try
            {
                ScriptSource script = engine.CreateScriptSourceFromFile(@scriptFile);
                var scriptResult = script.Execute(scope);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }

    }
}
