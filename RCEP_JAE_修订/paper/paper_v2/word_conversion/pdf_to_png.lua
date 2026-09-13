-- Word does not reliably render PDF images embedded by Pandoc.
-- Use the pre-rendered PNG counterpart when one is available.
function Image(el)
  if el.src:match("%.pdf$") then
    el.src = el.src:gsub("%.pdf$", ".png")
  end
  return el
end
