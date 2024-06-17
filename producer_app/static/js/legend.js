var svg_2 = d3.select("#legend")

svg_2.append("circle").attr("cx",200).attr("cy",130).attr("r", 6).style("fill", "#e41a1c")
svg_2.append("circle").attr("cx",200).attr("cy",160).attr("r", 6).style("fill", "#377eb8")
svg_2.append("circle").attr("cx",200).attr("cy",190).attr("r", 6).style("fill", "#4daf4a")
svg_2.append("text").attr("x", 220).attr("y", 130).text("Rugby").style("font-size", "15px").attr("alignment-baseline","middle")
svg_2.append("text").attr("x", 220).attr("y", 160).text("Football").style("font-size", "15px").attr("alignment-baseline","middle")
svg_2.append("text").attr("x", 220).attr("y", 190).text("Tennis").style("font-size", "15px").attr("alignment-baseline","middle")