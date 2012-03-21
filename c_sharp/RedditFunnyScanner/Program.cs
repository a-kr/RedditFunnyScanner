/*
 * Created by SharpDevelop.
 * User: Alexey
 * Date: 15.06.2010
 * Time: 21:03
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.IO;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;

namespace RedditFunnyScanner
{
	class Program
	{
		const string RedditUrl = @"http://www.reddit.com/r/funny/";
		static Regex rxLink = new Regex("<a class=\"title \" href=\"(.*?)\" >(.*?)</a>", RegexOptions.Compiled);
		static Regex rxNextPage = new Regex("<a href=\"(http://www.reddit.com/r/funny/.count=[0-9]+&amp;after=.*?)\"", RegexOptions.Compiled);
		
		public static void Main(string[] args)
		{
			new Program().Run();
		}
		
		void Run()
		{
			string url = RedditUrl;
			
			List<RedditLink> alllinks = new List<RedditLink>();
			
			while (true)
			{
				string page = PageGetter.GetPage(url);
				List<RedditLink> links = ProcessPage(page);
				alllinks.AddRange(links);
				string nextUrl = rxNextPage.Match(page).Groups[1].Value;
					
				if (nextUrl != "")
					url = nextUrl;
				else
					break;
			}
			
			string[] lines = (
				from link in alllinks 
				where link.Url.IndexOf(".jpg") > 0
				||  link.Url.IndexOf(".gif") > 0
				|| link.Url.IndexOf(".png") > 0
				|| link.Url.IndexOf("imgur.com") > 0
				select  string.Format("<p><a href=\"{0}\">{1}</a></p>", link.Url, link.Title)
			).ToArray();
			
			string filename = Path.GetTempFileName() + ".htm";
			File.WriteAllLines(filename, lines);
			
			System.Diagnostics.Process.Start(filename);
				
		}
		
		List<RedditLink> ProcessPage(string page)
		{
			var matches = rxLink.Matches(page);
			var list = new List<RedditLink>();
			
			foreach(Match match in matches)
			{
				list.Add(new RedditLink() { Url = match.Groups[1].Value, Title = match.Groups[2].Value });
			}
			
			return list;
		}
	}
	
	class RedditLink
	{
		public string Title { get; set; }
		public string Url { get; set; }
	}
}