---
tag: [Book, <%=`${book.title ? book.title.replaceAll(" ", "_") + "," : ""} ${book.authors ? book.authors.map(a => a.replaceAll(" ", "").replaceAll("　", "")).join(',') : ""}`%>]
title: "{{title}} {{subtitle}}"
subtitle: "{{subtitle}}"
aurhors: <%=book.authors ? book.authors.map(author => author.replaceAll(" ", "").replaceAll("　", "")).map(author=>`\n - ${author}`).join('') : ""%>
categories: <%=book.categories ? book.categories.map(category=>`\n - ${category}`).join('') : ""%>
publisher: {{publisher}}
publishDate: {{publishDate}}
totalPage: {{totalPage}}
coverUrl: {{coverUrl}}
description: {{description}}
link: {{link}}
isbn10: {{isbn10}}
isbn13: {{isbn13}}
status: unread
created: {{DATE:YYYY-MM-DD}}
updated: 
finished:
---
![cover|150]({{coverUrl}})

# {{title}} {{subtitle}}

<small>著者: {{author}}</small>  
<small>出版社: {{publisher}}</small>  
<small>出版日: {{publishDate}}</small>
