PLANTUML_JAR_URL = https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
DIAGRAMS_SRC := $(wildcard diagrams/*.plantuml)
DIAGRAMS_SVG := $(addsuffix .svg, $(basename $(DIAGRAMS_SRC)))

svg: plantuml.jar $(DIAGRAMS_SVG)

clean:
	rm -f plantuml.jar $(DIAGRAMS_PNG) $(DIAGRAMS_SVG)

plantuml.jar:
	curl -sSfL $(PLANTUML_JAR_URL) -o plantuml.jar

diagrams/%.svg: diagrams/%.plantuml
	java -jar plantuml.jar -tsvg $^

.PHONY: svg clean
