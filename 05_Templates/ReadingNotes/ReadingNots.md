---
tag: [Book, <%=`${book.title ? book.title.replaceAll(" ", "_") + "," : ""} ${book.authors ? book.authors.map(a => a.replaceAll(" ", "")).join(',') : ""}`%>]
title: "{{title}}"
subtitle: "{{subtitle}}"
author: {{author}}
aurhors: <%=book.authors ? book.authors.map(a => a.replaceAll(" ", "")).map(author=>`\n - ${author}`).join('') : ""%>
category: {{category}}
categories: <%=book.categories ? book.categories.map(category=>`\n - ${category}`).join('') : ""%>
publisher: {{publisher}}
publishDate: {{publishDate}}
totalPage: {{totalPage}}
coverUrl: {{coverUrl}}
coverSmallUrl: {{coverSmallUrl}}
description: {{description}}
link: {{link}}
previewLink: {{previewLink}}
isbn10: {{isbn10}}
isbn13: {{isbn13}}
status: unread
created: {{DATE:YYYY-MM-DD}}
updated: 
finished:
---
![cover|150]({{coverUrl}})

# {{title}}

<small>著者: {{author}}</small>  
<small>出版社: {{publisher}}</small>  
<small>出版日: {{publishDate}}</small>
