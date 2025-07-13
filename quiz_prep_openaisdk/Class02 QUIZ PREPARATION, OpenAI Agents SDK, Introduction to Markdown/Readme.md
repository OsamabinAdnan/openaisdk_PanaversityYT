# 👉 **Headings**

# Heading level 1

## Heading level 2

### Heading level 3

#### Heading level 4

##### Heading level 5

###### Heading level 6

After heading level 6, there will be normal text.

# 👉 **Alternate Syntax**
Alternatively, on the line below the text, add any number of == characters for heading level 1 or -- characters for heading level 2.

Heading level 1
===============

Heading level 2
---------------

# 👉 **Paragraphs**

To create paragraphs, use a blank line to separate one or more lines of text.

I really like using Markdown.

I think I'll use it to format all of my documents from now on.

# 👉 **Line Breaks**

To create a line break or new line (<br>), end a line with two or more spaces, and then type return.

# 👉 **Emphasis**

You can add emphasis by making text bold or italic.

## **Bold**

* I just love **bold text**.
* I just love __bold text__.
* Love **is** bold

## **Italic**

To italicize text, add one asterisk or underscore before and after a word or phrase. To italicize the middle of a word for emphasis, add one asterisk without spaces around the letters.

* Italicized text is the *cat's meow*.
* Italicized text is the _cat's meow_.
* A*cat*meow

## **Bold and Italic**

To emphasize text with **bold** and *italics* at the same time, add three asterisks or underscores before and after a word or phrase. To bold and italicize the middle of a word for emphasis, add three asterisks without spaces around the letters.

* This text is ***really important***.
* This text is ___really important___.
* This text is __*really important*__.
* This text is **_really important_**.
* This is really***very***important text.

# 👉 **Blockquotes**

To create a blockquote, add a > in front of a paragraph.

> Dorothy followed her through many of the beautiful rooms in her castle.

## **Blockquotes with Multiple Paragraphs**

Blockquotes can contain multiple paragraphs. Add a > on the blank lines between the paragraphs.

> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.

## **Nested Blockquotes**

Blockquotes can be nested. Add a >> in front of the paragraph you want to nest.

> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
>>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
>>>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.

## **Blockquotes with Other Elements**
Blockquotes can contain other Markdown formatted elements. Not all elements can be used — you’ll need to experiment to see which ones work.

> #### The quarterly results look great!
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
>  *Everything* is going according to **plan**.

## **Blockquotes Best Practices**

For compatibility, put blank lines before and after blockquotes.

# 👉 **Lists**

You can organize items into ordered and unordered lists.

## **Ordered Lists**

To create an ordered list, add line items with numbers followed by periods. The numbers don’t have to be in numerical order, but the list should start with the number one.

1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
    3. Indented item
        1. Sub-indented item
        2. Sub-indented item
4. Fourth item

## **Unordered Lists**

To create an unordered list, add dashes (-), asterisks (*), or plus signs (+) in front of line items. Indent one or more items to create a nested list.

- First item
- Second item
* Third item
* Fourth item
+ Fifth item
+ Sixth item

---

- First item
- Second item
- Third item
    + Indented item
    + Indented item
        * Sub-indented item
        * Sub-indented item
            - Sub-indented item
            - Sub-indented item
- Fourth item

## **Starting Unordered List Items With Numbers**

If you need to start an unordered list item with a number followed by a period, you can use a backslash (\) to escape the period.

- 1968\. A great year!
- I think 1969 was second best.

## **Adding Elements in Lists**

To add another element in a list while preserving the continuity of the list, indent the element four spaces or one tab, as shown in the following examples.

### **Paragraphs**

* This is the first list item.
* Here's the second list item.

    I need to add another paragraph below the second list item.

* And here's the third list item.

### **Blockquotes**

* This is the first list item.
* Here's the second list item.

    > A blockquote would look great below the second list item.

* And here's the third list item.

# 👉 **Code Blocks**

Code blocks are normally indented four spaces or one tab. When they’re in a list, indent them eight spaces or two tabs.

1. Open the file.
2. Find the following code block on line 21:

        <html>
          <head>
            <title>Test</title>
          </head>

3. Update the title to match the name of your website.

4. Below is python code

    ```python

    import requests
    response = requests.get('https://api.github.com')
    print(response.status_code)

    ```

5. Below is JavaScript code

    ```JavaScript

    x = 5;
    y = 6;
    console.log(x + y);
    
    ```

# 👉 **Code**

To denote a word or phrase as code, enclose it in backticks (`).

At the command prompt, type `nano`.

## **Escaping Backticks**

If the word or phrase you want to denote as code includes one or more backticks, you can escape it by enclosing the word or phrase in double backticks (``).

``Use `code` in your Markdown file.``

## **Code Blocks**
To create code blocks, indent every line of the block by at least four spaces or one tab.
    
    <html>
      <head>
      </head>
    </html>

```html
    <html>
      <head>
      </head>
    </html>
```

# 👉 **Horizontal Rules**
To create a horizontal rule, use three or more asterisks (***), dashes (---), or underscores (___) on a line by themselves.

***

---

___

# 👉 **Links**

To create a link, enclose the link text in brackets (e.g., [Duck Duck Go]) and then follow it immediately with the URL in parentheses (e.g., (https://duckduckgo.com)).

My favorite search engine is [Duck Duck Go](https://duckduckgo.com).

## **Adding Titles**

You can optionally add a title for a link. This will appear as a tooltip when the user hovers over the link. To add a title, enclose it in quotation marks after the URL.

My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").

## **URLs and Email Addresses**
To quickly turn a URL or email address into a link, enclose it in angle brackets.

<https://www.markdownguide.org>

<fake@example.com>

## **Formatting Links**

To emphasize links, add asterisks before and after the brackets and parentheses. To denote links as code, add backticks in the brackets.

I love supporting the **[EFF](https://eff.org "This is https://eff.org")**.

This is the *[Markdown Guide](https://www.markdownguide.org)*.

See the section on [`code`](#code).

## **Reference-style Links**

Reference-style links are a special kind of link that make URLs easier to display and read in Markdown. Reference-style links are constructed in two parts: the part you keep inline with your text and the part you store somewhere else in the file to keep the text easy to read.

Say you add a URL as a standard URL link to a paragraph and it looks like this in Markdown:

In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends
of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to
eat: it was a [hobbit-hole](https://en.wikipedia.org/wiki/Hobbit#Lifestyle "Hobbit lifestyles"), and that means comfort.

Another example:

In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends
of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to
eat: it was a [hobbit-hole][1], and that means comfort.

[1]:<https://en.wikipedia.org/wiki/Hobbit#Lifestyle> "Hobbit lifestyles"

# 👉 **Images**

To add an image, add an exclamation mark (!), followed by alt text in brackets, and the path or URL to the image asset in parentheses. You can optionally add a title in quotation marks after the path or URL.

1. Open the file containing the Linux mascot.
2. Marvel at its beauty.

    ![Tux, the Linux mascot](https://mdg.imgix.net/assets/images/tux.png?auto=format&fit=clip&q=40&w=100)

3. Close the file.

Another example:

![The San Juan Mountains are beautiful!](https://mdg.imgix.net/assets/images/san-juan-mountains.jpg?auto=format&fit=clip&q=40&w=1080 "San Juan Mountains")

## **Linking Images**

To add a link to an image, enclose the Markdown for the image in brackets, and then add the link in parentheses.

[![An old rock in the desert](https://mdg.imgix.net/assets/images/shiprock.jpg?auto=format&fit=clip&q=40&w=1080 "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)

# 👉 **Escaping Characters**

To display a literal character that would otherwise be used to format text in a Markdown document, add a backslash (\) in front of the character.

\* Without the backslash, this would be a bullet in an unordered list

## **Characters You Can Escape**

You can use a backslash to escape the following characters.

| Character | Name |
|-----------|------|
| \\        | Backslash |
| \`        | Backtick (see also [escaping backticks in code](https://www.markdownguide.org/basic-syntax/#escaping-backticks)) |
| \*        | Asterisk |
| \_        | Underscore |
| \{ \}     | Curly brace |
| \[ \]     | Square bracket |
| \( \)     | Parenthesis |
| \< \>     | Angle bracket |
| \#        | Pound sign |
| \+        | Plus sign |
| \-        | Minus sign |
| \.        | Dot |
| \!        | Exclamation mark |
| \|        | Pipe (see also [escaping pipes in tables](https://www.markdownguide.org/extended-syntax/#escaping-pipe-characters-in-tables))|

