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
    | 'math_block_dollar'
    | 'math_block_bracket'
    | 'math_inline_dollar'
    | 'math_inline_paren'
    | 'inline_code'
    | 'code_block'
    | 'markdown_link'
    | 'bold_italic'
    | 'bold'
    | 'italic'
    | 'strikethrough';
  raw: string;
  content: string;
  extra?: string; // URL for links, language for code blocks
}

/**
 * Tokenizes a string containing KaTeX math and Markdown syntax into structured tokens.
 */
function tokenizeText(text: string): Token[] {
  if (!text) return [];

  const tokenPatterns: Array<{
    type: Token['type'];
    regex: RegExp;
  }> = [
    { type: 'code_block', regex: /```(?:[a-zA-Z0-9_-]+)?\n?([\s\S]*?)```/ },
    { type: 'math_block_dollar', regex: /\$\$([\s\S]*?)\$\$/ },
    { type: 'math_block_bracket', regex: /\\\[([\s\S]*?)\\\]/ },
    { type: 'inline_code', regex: /`([^`\n]+?)`/ },
    { type: 'math_inline_dollar', regex: /\$([^\$\n]+?)\$/ },
    { type: 'math_inline_paren', regex: /\\\(([^\n]+?)\\\)/ },
    { type: 'markdown_link', regex: /\[([^\]\n]+)\]\((https?:\/\/[^\s\)]+|[^\s\)]+)\)/ },
    { type: 'bold_italic', regex: /(?:\*\*\*|___)([^\*\n]+?)(?:\*\*\*|___)/ },
    { type: 'bold', regex: /(?:\*\*|__)([^\*\n]+?)(?:\*\*|__)/ },
    { type: 'strikethrough', regex: /~~([^~\n]+?)~~/ },
    { type: 'italic', regex: /(?:^|[^\*\w])\*([^\*\n\s](?:[^\*\n]*?[^\*\n\s])?)\*(?=[^\*\w]|$)/ },
  ];

  const tokens: Token[] = [];
  let remaining = text;

  while (remaining.length > 0) {
    let earliestMatch: RegExpMatchArray | null = null;
    let earliestIndex = Infinity;
    let matchingPattern: { type: Token['type']; regex: RegExp } | null = null;

    for (const p of tokenPatterns) {
      const match = remaining.match(p.regex);
      if (match && match.index !== undefined) {
        let matchIndex = match.index;
        // For italic pattern with leading boundary character
        if (p.type === 'italic' && match[0].indexOf('*') > 0) {
          matchIndex += match[0].indexOf('*');
        }

        if (matchIndex < earliestIndex) {
          earliestIndex = matchIndex;
          earliestMatch = match;
          matchingPattern = p;
        }
      }
    }

    if (earliestMatch && matchingPattern) {
      if (earliestIndex > 0) {
        tokens.push({
          type: 'text',
          raw: remaining.slice(0, earliestIndex),
          content: remaining.slice(0, earliestIndex),
        });
      }

      const raw =
        matchingPattern.type === 'italic' && earliestMatch[0].indexOf('*') > 0
          ? remaining.slice(earliestIndex, earliestIndex + (earliestMatch[1]?.length || 0) + 2)
          : earliestMatch[0];

      tokens.push({
        type: matchingPattern.type,
        raw,
        content: earliestMatch[1] ?? '',
        extra: earliestMatch[2],
      });

      remaining = remaining.slice(earliestIndex + raw.length);
    } else {
      tokens.push({
        type: 'text',
        raw: remaining,
        content: remaining,
      });
      break;
    }
  }

  return tokens;
}

/**
 * Recursively renders tokens to React elements.
 */
function renderNodes(text: string, keyPrefix = 'r', depth = 0): React.ReactNode[] {
  if (!text) return [];
  if (depth > 5) return [text];

  const tokens = tokenizeText(text);

  return tokens.map((token, idx) => {
    const key = `${keyPrefix}-${depth}-${idx}`;

    switch (token.type) {
      case 'math_block_dollar':
      case 'math_block_bracket': {
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

      case 'math_inline_dollar':
      case 'math_inline_paren': {
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
