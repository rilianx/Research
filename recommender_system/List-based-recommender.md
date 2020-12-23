---


---

<h1 id="sistema-de-recomendación-basado-en-grafo-bipartito">Sistema de recomendación basado en grafo bipartito</h1>
<p>El objetivo del algoritmo es recomendar películas en base a un pequeño conjunto de películas de origen o <em>películas fuente</em>.</p>
<p>Imaginemos que cada película fuente tiene una esencia o <em>color</em>. La idea del algoritmo es:</p>
<ol>
<li>Propagar estos colores a través de las otras películas del grafo. El grafo se comporta similar a una <em>cadena de Markov</em>. En cada iteración, los últimos valores propagados se propagan a los nodos adyacentes.</li>
<li>Recomendar las películas con mayor diversidad de colores.</li>
</ol>
<p>Aquí unas figuras de ejemplo.<br>
<strong>Grafo inicial</strong>. Los nodos de colores representan las películas de partida.<br>
<img src="https://i.imgur.com/EFoqWBu.png" alt="image"></p>
<p>Grafo luego de propagar los <em>colores</em> por algunas iteraciones.<br>
Los nodos más grandes representan las películas con mayor <em>variedad de colores</em>.<br>
<img src="https://i.imgur.com/5B7ZvZj.png" alt="image"></p>
<h2 id="el-algoritmo">El algoritmo</h2>
<p>Sea <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>F</mi></mrow><annotation encoding="application/x-tex">F</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.68333em; vertical-align: 0em;"></span><span class="mord mathdefault" style="margin-right: 0.13889em;">F</span></span></span></span></span> el conjunto de películas fuente.<br>
El grafo es bipartito, que se compone de nodos de tipo <em>Película</em> y nodos de tipo <em>Lista de pelis</em>. Los nodos de tipo película <code>m</code>cuentan con dos atributos importantes:</p>
<ul>
<li><code>color[m]</code>    Vector con valores en <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mo stretchy="false">[</mo><mn>0</mn><mo separator="true">,</mo><mn>1</mn><mo stretchy="false">]</mo></mrow><annotation encoding="application/x-tex">[0,1]</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mopen">[</span><span class="mord">0</span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">1</span><span class="mclose">]</span></span></span></span></span>, que indican la presencia de cada uno de los colores de las películas fuente.</li>
<li><code>P[m]</code> Vector con el valor que se debe propagar en la siguiente iteración o <em>timestep</em> del algoritmo</li>
</ul>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">import</span> numpy <span class="token keyword">as</span> np

<span class="token keyword">def</span> <span class="token function">main</span><span class="token punctuation">(</span>F<span class="token punctuation">,</span> M<span class="token punctuation">,</span> steps<span class="token operator">=</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
  <span class="token comment">#inicalizando la fuente</span>
  P <span class="token operator">=</span> <span class="token builtin">dict</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
  <span class="token keyword">for</span> m <span class="token keyword">in</span> F<span class="token punctuation">:</span>
     color<span class="token punctuation">[</span>m<span class="token punctuation">]</span> <span class="token operator">=</span> np<span class="token punctuation">.</span>array<span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>F<span class="token punctuation">)</span><span class="token punctuation">)</span>
	 color<span class="token punctuation">[</span>m<span class="token punctuation">]</span><span class="token punctuation">[</span>F<span class="token punctuation">.</span>index<span class="token punctuation">(</span>m<span class="token punctuation">)</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">1.0</span>
     P<span class="token punctuation">[</span>m<span class="token punctuation">]</span> <span class="token operator">=</span> np<span class="token punctuation">.</span>array<span class="token punctuation">(</span><span class="token builtin">len</span><span class="token punctuation">(</span>F<span class="token punctuation">)</span><span class="token punctuation">)</span>
	 P<span class="token punctuation">[</span>m<span class="token punctuation">]</span><span class="token punctuation">[</span>F<span class="token punctuation">.</span>index<span class="token punctuation">(</span>m<span class="token punctuation">)</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token number">1.0</span> 
	 
  <span class="token comment">#propagación por algunas iteraciones</span>
  <span class="token keyword">for</span> timestep <span class="token keyword">in</span> <span class="token builtin">range</span><span class="token punctuation">(</span>steps<span class="token punctuation">)</span><span class="token punctuation">:</span>
	P<span class="token operator">=</span> propagate<span class="token punctuation">(</span>P<span class="token punctuation">)</span>
	
  <span class="token comment">#recomendación</span>
  <span class="token keyword">return</span> recommend<span class="token punctuation">(</span>M<span class="token punctuation">)</span>
</code></pre>
<p>Notar <code>F</code> es una lista con las películas fuente. Por lo que al colocar: <code>color[m][F.index(m)]=1.0</code>, estamos creando un vector: <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mo stretchy="false">[</mo><mn>0</mn><mo separator="true">,</mo><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi><mo separator="true">,</mo><mn>1</mn><mo separator="true">,</mo><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi><mi mathvariant="normal">.</mi><mo separator="true">,</mo><mn>0</mn><mo stretchy="false">]</mo></mrow><annotation encoding="application/x-tex">[0,...,1,...,0]</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mopen">[</span><span class="mord">0</span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">.</span><span class="mord">.</span><span class="mord">.</span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">1</span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">.</span><span class="mord">.</span><span class="mord">.</span><span class="mpunct">,</span><span class="mspace" style="margin-right: 0.166667em;"></span><span class="mord">0</span><span class="mclose">]</span></span></span></span></span> donde el <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mn>1</mn></mrow><annotation encoding="application/x-tex">1</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.64444em; vertical-align: 0em;"></span><span class="mord">1</span></span></span></span></span> se encuentra en la posición correspondiente a la película fuente en la lista <code>F</code>. Lo mismo ocurre con <code>c_propag</code>. <code>M</code> es la colección con todas las películas.</p>
<p><code>P</code> es un diccionario que guarda en cada iteración la películas que debieran propagar sus valores. Cada película se asocia al vector de colores que se debe propagar.</p>
<p>La función <code>propagate</code> propaga los cambios a partir del diccionario de películas <code>P</code> y retorna un nuevo diccionario con las películas modificadas para seguir propagando.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">propagate</span><span class="token punctuation">(</span>P<span class="token punctuation">,</span> t_factor<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
  P2 <span class="token operator">=</span> <span class="token builtin">dict</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment">#películas que se propagarán en </span>
                <span class="token comment"># la siguiente iteración</span>
  <span class="token keyword">for</span> each m <span class="token keyword">in</span> P<span class="token punctuation">:</span>
     <span class="token keyword">for</span> each l <span class="token keyword">in</span> adj_lists<span class="token punctuation">(</span>m<span class="token punctuation">)</span><span class="token punctuation">:</span>
       <span class="token keyword">for</span> each adj_m <span class="token keyword">in</span> l<span class="token punctuation">.</span>movies<span class="token punctuation">:</span>
         size_list <span class="token operator">=</span> <span class="token builtin">len</span><span class="token punctuation">(</span>l<span class="token punctuation">.</span>movies<span class="token punctuation">)</span>
         propag_value <span class="token operator">=</span> <span class="token punctuation">(</span>P<span class="token punctuation">[</span>m<span class="token punctuation">]</span><span class="token operator">*</span>t_factor<span class="token punctuation">)</span><span class="token operator">/</span>size_list
         P2<span class="token punctuation">[</span>adj_m<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token builtin">max</span><span class="token punctuation">(</span>propag_value<span class="token punctuation">,</span> P<span class="token punctuation">[</span>adj_m<span class="token punctuation">]</span><span class="token punctuation">)</span> 

  <span class="token comment">#se actualiza el color de las películas</span>
  <span class="token keyword">for</span> each m <span class="token keyword">in</span> P2<span class="token punctuation">:</span> color<span class="token punctuation">[</span>m<span class="token punctuation">]</span> <span class="token operator">+=</span> P2<span class="token punctuation">[</span>m<span class="token punctuation">]</span>
  
  <span class="token keyword">return</span> P2
</code></pre>
<p><code>t_factor</code> es la tasa de propagación de los colores de un nodo a otro.</p>
<p>La función <code>recommend(G)</code> debería usar algún criterio para entregar una lista de películas en base a sus colores. Idealmente queremos maximizar todos los colores del vector, ya que valores altos para <strong>todos los colores</strong> indicarían que la película se parece a todas las películas fuente.</p>
<p>La función propuesta simplemente retorna la película que <strong>maximiza el mínimo valor del vector</strong>.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">recommend</span><span class="token punctuation">(</span>M<span class="token punctuation">)</span><span class="token punctuation">:</span>
  maxmin<span class="token operator">=</span><span class="token number">0.0</span>
  <span class="token keyword">for</span> each m <span class="token keyword">in</span> M<span class="token punctuation">.</span>movies<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    min_color <span class="token operator">=</span> np<span class="token punctuation">.</span><span class="token builtin">min</span><span class="token punctuation">(</span>color<span class="token punctuation">[</span>m<span class="token punctuation">]</span><span class="token punctuation">)</span>
    <span class="token keyword">if</span> min_color <span class="token operator">&gt;</span> maxmin<span class="token punctuation">:</span>
      maxmin <span class="token operator">=</span> min_color
      rec_movie <span class="token operator">=</span> m
  <span class="token keyword">return</span> rec_movie<span class="token punctuation">,</span> maxmin
</code></pre>
<h2 id="validación">Validación</h2>
<p>Para validar el o los métodos propongo el siguiente experimento.</p>
<ol>
<li><em>Seleccionar unas 10 listas de menos de 20 películas para probar el sistema</em>.</li>
<li>Aplicar el algoritmo a partir de un subconjunto de películas de cada lista (películas fuente). Obtener el <em>porcentaje de acierto</em> (número de películas recomendadas vs. número de películas en lista de películas fuente).</li>
</ol>

