using System;

namespace comp
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var file1 = args[0];
            var file2 = args[1];
            var myRand = new Random();
            Console.Write(myRand.Next() % 100 > 30);
        }
    }
}