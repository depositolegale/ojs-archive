wget.callbacks.get_urls = function(file, url, is_css, iri)
  local urls = {}
  if string.match(url, "article/download") then
      view_url = string.gsub(url, "download", "view")
      table.insert(urls, { url=view_url })
  end
  return urls
end
