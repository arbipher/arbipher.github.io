function Inlines(inlines)
  local result = {}
  local i = 1

  while i <= #inlines do
    local el = inlines[i]

    -- 🟢 Case 1: fully self-contained ::...::n
    if el.t == "Str" then
      local phrase, index = string.match(el.text, "^::(.+)::(%d+)$")
      if phrase and index then
        table.insert(result, pandoc.Span(
          { pandoc.Str(phrase) },
          { ["class"] = "fragment", ["data-fragment-index"] = index }
        ))
        i = i + 1
        goto continue
      end
    end

    -- 🔵 Case 2: fragment span starts here ::...
    if el.t == "Str" and string.sub(el.text, 1, 2) == "::" then
      local buffer = {}
      local index = nil
      local first = string.sub(el.text, 3)
      if first ~= "" then table.insert(buffer, pandoc.Str(first)) end
      i = i + 1

      while i <= #inlines do
        local next_el = inlines[i]
        if next_el.t == "Str" then
          local frag_text, idx = string.match(next_el.text, "^(.-)::(%d+)$")
          if idx then
            if frag_text ~= "" then table.insert(buffer, pandoc.Str(frag_text)) end
            index = idx
            i = i + 1
            break
          end
        end
        table.insert(buffer, next_el)
        i = i + 1
      end

      if index then
        table.insert(result, pandoc.Span(buffer, {
          ["class"] = "fragment",
          ["data-fragment-index"] = index
        }))
        goto continue
      else
        for _, b in ipairs(buffer) do table.insert(result, b) end
      end
    end

    table.insert(result, el)
    i = i + 1
    ::continue::
  end

  return result
end


function Div(el)
  for _, cls in ipairs(el.classes) do
    local index = string.match(cls, "^fff%-(%d+)$")
    if index then
      el.attributes["data-fragment-index"] = index
      -- 确保含有 fragment 类
      local has_fragment = false
      for _, c in ipairs(el.classes) do
        if c == "fragment" then
          has_fragment = true
          break
        end
      end
      if not has_fragment then
        table.insert(el.classes, "fragment")
      end
    end
  end
  return el
end
