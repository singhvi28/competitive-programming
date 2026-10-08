import React, { useMemo } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

interface MathRendererProps {
  text: string;
  className?: string;
}

interface Token {
  type:
    | 'text'
    | 'math_block'
    | 'math_inline'
    | 'inline_code'
    | 'code_block'
    | 'markdown_link'
    | 'bold_italic'
    | 'bold'
    | 'italic'
    | 'strikethrough';
  raw: string;
  content: string;
  extra?: string; // URL for links, etc.
}

/**
 * Deterministic sequential scanner that parses KaTeX math ($$, \[, $, \()
 * and Markdown (```, `, ***, **, ~~, *, links) without regex delimiter collisions.
 */
function tokenizeText(text: string): Token[] {
  if (!text) return [];

  const tokens: Token[] = [];
  let i = 0;
  const n = text.length;

  while (i < n) {
    // 1. Block Math $$...$$
    if (text.startsWith('$$', i)) {
      const end = text.indexOf('$$', i + 2);
      if (end !== -1) {
        tokens.push({
          type: 'math_block',
          content: text.slice(i + 2, end),
          raw: text.slice(i, end + 2),
        });
        i = end + 2;
        continue;
      }
    }

    // 2. Block Math \[...\]
    if (text.startsWith('\\[', i)) {
      const end = text.indexOf('\\]', i + 2);
      if (end !== -1) {
        tokens.push({
          type: 'math_block',
          content: text.slice(i + 2, end),
          raw: text.slice(i, end + 2),
        });
        i = end + 2;
        continue;
      }
    }

    // 3. Fenced Code ```...```
    if (text.startsWith('```', i)) {
      const end = text.indexOf('```', i + 3);
      if (end !== -1) {
        let blockContent = text.slice(i + 3, end);
        const firstNl = blockContent.indexOf('\n');
        if (firstNl !== -1 && firstNl < 15 && !blockContent.slice(0, firstNl).includes(' ')) {
          blockContent = blockContent.slice(firstNl + 1);
        }
        tokens.push({
          type: 'code_block',
          content: blockContent,
          raw: text.slice(i, end + 3),
        });
        i = end + 3;
        continue;
      }
    }

    // 4. Inline Code `...`
    if (text[i] === '`') {
      const end = text.indexOf('`', i + 1);
      if (end !== -1 && !text.slice(i + 1, end).includes('\n')) {
        tokens.push({
          type: 'inline_code',
          content: text.slice(i + 1, end),
          raw: text.slice(i, end + 1),
        });
        i = end + 1;
        continue;
      }
    }

    // 5. Bold+Italic ***...*** or ___...___
    if (text.startsWith('***', i) || text.startsWith('___', i)) {
      const delim = text.slice(i, i + 3);
      const end = text.indexOf(delim, i + 3);
      if (end !== -1 && !text.slice(i + 3, end).includes('\n')) {
        tokens.push({
          type: 'bold_italic',
          content: text.slice(i + 3, end),
          raw: text.slice(i, end + 3),
        });
        i = end + 3;
        continue;
      }
    }

    // 6. Bold **...** or __...__
    if (text.startsWith('**', i) || text.startsWith('__', i)) {
      const delim = text.slice(i, i + 2);
      const end = text.indexOf(delim, i + 2);
      if (end !== -1 && !text.slice(i + 2, end).includes('\n')) {
        tokens.push({
          type: 'bold',
          content: text.slice(i + 2, end),
          raw: text.slice(i, end + 2),
        });
        i = end + 2;
        continue;
      }
    }

    // 7. Strikethrough ~~...~~
    if (text.startsWith('~~', i)) {
      const end = text.indexOf('~~', i + 2);
      if (end !== -1 && !text.slice(i + 2, end).includes('\n')) {
        tokens.push({
          type: 'strikethrough',
          content: text.slice(i + 2, end),
          raw: text.slice(i, end + 2),
        });
        i = end + 2;
        continue;
      }
    }

    // 8. Markdown Links [text](url)
    if (text[i] === '[') {
      const closeBracket = text.indexOf(']', i + 1);
      if (closeBracket !== -1 && text[closeBracket + 1] === '(') {
        const closeParen = text.indexOf(')', closeBracket + 2);
        if (closeParen !== -1 && !text.slice(i, closeParen + 1).includes('\n')) {
          const linkText = text.slice(i + 1, closeBracket);
          const linkUrl = text.slice(closeBracket + 2, closeParen);
          tokens.push({
            type: 'markdown_link',
            content: linkText,
            extra: linkUrl,
            raw: text.slice(i, closeParen + 1),
          });
          i = closeParen + 1;
          continue;
        }
      }
    }

    // 9. Inline Math \(...\)
    if (text.startsWith('\\(', i)) {
      const end = text.indexOf('\\)', i + 2);
      if (end !== -1 && !text.slice(i + 2, end).includes('\n')) {
        tokens.push({
          type: 'math_inline',
          content: text.slice(i + 2, end),
          raw: text.slice(i, end + 2),
        });
        i = end + 2;
        continue;
      }
    }

    // 10. Inline Math $...$
    if (text[i] === '$') {
      const end = text.indexOf('$', i + 1);
      if (end !== -1 && end > i + 1 && !text.slice(i + 1, end).includes('\n')) {
        tokens.push({
          type: 'math_inline',
          content: text.slice(i + 1, end),
          raw: text.slice(i, end + 1),
        });
        i = end + 1;
        continue;
      }
    }

    // 11. Italic *...* or _..._
    if ((text[i] === '*' || text[i] === '_') && (i === 0 || /\s|[^\w]/.test(text[i - 1]))) {
      const delim = text[i];
      const end = text.indexOf(delim, i + 1);
      if (
        end !== -1 &&
        end > i + 1 &&
        !text.slice(i + 1, end).includes('\n') &&
        (end === n - 1 || /\s|[^\w]/.test(text[end + 1])) &&
        !/\s/.test(text[i + 1]) &&
        !/\s/.test(text[end - 1])
      ) {
        tokens.push({
          type: 'italic',
          content: text.slice(i + 1, end),
          raw: text.slice(i, end + 1),
        });
        i = end + 1;
        continue;
      }
    }

    // Accumulate plain text until next token start
    let nextSpecial = n;
    const specials = ['$$', '\\[', '\\(', '```', '`', '***', '___', '**', '__', '~~', '[', '$'];
    for (const sp of specials) {
      const pos = text.indexOf(sp, i);
      if (pos !== -1 && pos < nextSpecial) {
        nextSpecial = pos;
      }
    }

    for (let j = i; j < nextSpecial; j++) {
      if (text[j] === '*' || text[j] === '_') {
        if (j === 0 || /\s|[^\w]/.test(text[j - 1])) {
          nextSpecial = j;
          break;
        }
      }
    }

    if (nextSpecial > i) {
      tokens.push({
        type: 'text',
        content: text.slice(i, nextSpecial),
        raw: text.slice(i, nextSpecial),
      });
      i = nextSpecial;
    } else {
      tokens.push({
        type: 'text',
        content: text[i],
        raw: text[i],
      });
      i++;
    }
  }

  return tokens;
}

/**
 * Recursively renders tokens into React elements.
 */
function renderNodes(text: string, keyPrefix = 'r', depth = 0): React.ReactNode[] {
  if (!text) return [];
  if (depth > 5) return [text];

  const tokens = tokenizeText(text);

  return tokens.map((token, idx) => {
    const key = `${keyPrefix}-${depth}-${idx}`;

    switch (token.type) {
      case 'math_block': {
        const math = token.content.trim();
        try {
          const html = katex.renderToString(math, {
            displayMode: true,
            throwOnError: false,
          });
          return (
            <span
              key={key}
              className="block my-2 overflow-x-auto text-slate-100"
              dangerouslySetInnerHTML={{ __html: html }}
            />
          );
        } catch {
          return (
            <span key={key} className="text-red-400 font-mono block my-2">
              {token.raw}
            </span>
          );
        }
      }

      case 'math_inline': {
        const math = token.content.trim();
        try {
          const html = katex.renderToString(math, {
            displayMode: false,
            throwOnError: false,
          });
          return (
            <span
              key={key}
              className="inline-block text-slate-100"
              dangerouslySetInnerHTML={{ __html: html }}
            />
          );
        } catch {
          return (
            <span key={key} className="text-red-400 font-mono">
              {token.raw}
            </span>
          );
        }
      }

      case 'inline_code': {
        return (
          <code
            key={key}
            className="px-1.5 py-0.5 mx-0.5 rounded bg-slate-800/90 text-amber-300 font-mono text-[0.875em] border border-slate-700/60 font-medium break-words inline-block"
          >
            {token.content}
          </code>
        );
      }

      case 'code_block': {
        return (
          <pre
            key={key}
            className="p-3.5 my-2.5 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs overflow-x-auto text-slate-200"
          >
            <code>{token.content}</code>
          </pre>
        );
      }

      case 'bold_italic': {
        return (
          <strong key={key} className="font-bold italic text-white">
            {renderNodes(token.content, `${key}-bi`, depth + 1)}
          </strong>
        );
      }

      case 'bold': {
        return (
          <strong key={key} className="font-bold text-white">
            {renderNodes(token.content, `${key}-b`, depth + 1)}
          </strong>
        );
      }

      case 'italic': {
        return (
          <em key={key} className="italic text-slate-200">
            {renderNodes(token.content, `${key}-i`, depth + 1)}
          </em>
        );
      }

      case 'strikethrough': {
        return (
          <del key={key} className="line-through text-slate-500">
            {renderNodes(token.content, `${key}-s`, depth + 1)}
          </del>
        );
      }

      case 'markdown_link': {
        return (
          <a
            key={key}
            href={token.extra || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-400 hover:text-indigo-300 underline underline-offset-2 font-medium inline-flex items-center gap-0.5"
          >
            {renderNodes(token.content, `${key}-l`, depth + 1)}
          </a>
        );
      }

      case 'text':
      default:
        return <React.Fragment key={key}>{token.content}</React.Fragment>;
    }
  });
}

export const MathRenderer: React.FC<MathRendererProps> = ({ text, className = '' }) => {
  const renderedElements = useMemo(() => {
    if (!text) return null;
    return renderNodes(text);
  }, [text]);

  return <span className={className}>{renderedElements}</span>;
};
