import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import remarkInlineFootnote from "remark-inline-footnote"

const config = await loadQuartzConfig()

config.plugins.transformers.push({
  name: "ObsidianInlineFootnotes",
  markdownPlugins() {
    return [remarkInlineFootnote]
  },
})

export default config
export const layout = await loadQuartzLayout()
