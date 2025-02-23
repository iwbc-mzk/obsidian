---
tag: [📚Book, "{{title}}", <%=book.authors.map(author=>`"${author}"`).join(',')%>]
title: "{{title}}"
subtitle: "{{subtitle}}"
author: {{author}}
aurhors: <%=book.authors.map(author=>`\n - ${author}`).join('')%>
category: {{category}}
categories: <%=book.categories.map(category=>`\n - ${category}`).join('')%>
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
finished:
---
![cover|150]({{coverUrl}})

# {{title}}

author: {{author}}  
publisher: {{publisher}}  
publish: {{publishDate}}
