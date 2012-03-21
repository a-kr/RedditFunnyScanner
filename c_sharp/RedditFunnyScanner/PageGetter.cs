/*
 * Created by SharpDevelop.
 * User: Alexey
 * Date: 15.06.2010
 * Time: 21:14
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Net;
using System.IO;

namespace RedditFunnyScanner
{
	/// <summary>
	/// Description of PageGetter.
	/// </summary>
	public class PageGetter
	{
		public static string GetPage(string Url)
		{
					// Open a connection
		    HttpWebRequest WebRequestObject = (HttpWebRequest)HttpWebRequest.Create(Url);
		 
		    // You can also specify additional header values like 
		    // the user agent or the referer:
		    WebRequestObject.UserAgent	= ".NET Framework/2.0";
		    WebRequestObject.Referer	= "http://www.example.com/";
		 
		    // Request response:
		    WebResponse Response = WebRequestObject.GetResponse();
		 
		    // Open data stream:
		    Stream WebStream = Response.GetResponseStream();
		 
		    // Create reader object:
		    StreamReader Reader = new StreamReader(WebStream);
		 
		    // Read the entire stream content:
		    string PageContent = Reader.ReadToEnd();
		 
		    // Cleanup
		    Reader.Close();
		    WebStream.Close();
		    Response.Close();
		 
		    return PageContent;
		}
	}
}
