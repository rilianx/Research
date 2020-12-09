---


---

<h1 id="ipopt-para-ibexopt">IpOPT para IbexOpt</h1>
<p>Upper bounding is a very important component of branch &amp; bound solvers for global optimization. Finding good quality solutions early in the search may improve the performance of the solver by means of the addition of the auxiliary constraint <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>f</mi><mo stretchy="false">(</mo><mi>x</mi><mo stretchy="false">)</mo><mo>&lt;</mo><mi>u</mi><mi>b</mi></mrow><annotation encoding="application/x-tex">f(x)&lt;ub</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 1em; vertical-align: -0.25em;"></span><span class="mord mathdefault" style="margin-right: 0.10764em;">f</span><span class="mopen">(</span><span class="mord mathdefault">x</span><span class="mclose">)</span><span class="mspace" style="margin-right: 0.277778em;"></span><span class="mrel">&lt;</span><span class="mspace" style="margin-right: 0.277778em;"></span></span><span class="base"><span class="strut" style="height: 0.69444em; vertical-align: 0em;"></span><span class="mord mathdefault">u</span><span class="mord mathdefault">b</span></span></span></span></span>, where <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><mi>u</mi><mi>b</mi></mrow><annotation encoding="application/x-tex">ub</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.69444em; vertical-align: 0em;"></span><span class="mord mathdefault">u</span><span class="mord mathdefault">b</span></span></span></span></span> is the cost of the best found solution so far.</p>
<p>IpOPT is a well know local optimizer that can be used for finding solutions in B&amp;B global optimizers, however it is too expensive to be called in each node of the search tree.</p>
<p>In this work, we propose a mechanism for applying IpOPT only in some nodes of the search tree in order to avoid a large time overhead but keeping the effectiveness of the method.</p>
<blockquote>
<p><a href="https://docs.google.com/document/d/1P0yYlNuIu-I2taOfEJMDzq-FMiMf7y_uyqXVvFZ8ssE/edit#">TODO</a> ∙ <a href="http://mpc.zib.de/archive/2018/3/Khajavirad-Sahinidis2018_Article_AHybridLPNLPParadigmForGlobalO.pdf">PaperBaron</a> ∙  <a href="https://drive.google.com/file/d/15M62Oc7JNeRiitNUULc4hmM8KtAzBlF6/view?usp=sharing">Resultados</a></p>
</blockquote>
<p>Actualmente tenemos 3 variantes:</p>
<ul>
<li>Ipopt sólo</li>
<li>Ipopt para encontrar solución inicial, luego IbexOpt</li>
<li>IbexOpt con Ipopt para buscar soluciones</li>
</ul>
<p><strong>TODO</strong></p>
<ul>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Arreglar tabla de resultados para que sea fácil de comparar.
<ul>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> ¿En qué instancias IpOPT da buenos resultados?</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> ¿En qué instancias no da tan buenos resultados?</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Ibex vs IpOPTonly vs IpOPT+Ibex (initial_loup)</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Revisar que los tiempos tengan sentido</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Tabla con toda la info y tabla con información reducida</li>
</ul>
</li>
</ul>
<p>inst|f(x*)|Ibx(t)|Ibx(#cells)|IpOpt(t)|IpOpt(loup)|IL(t1)|IL(t2)|IL(#cells)|<br>
|–|--|–|--|–|--|–|--|–||–|--|</p>
<ul>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Diseñar mecanismo para seleccionar cuándo aplicar Ipopt.</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> ¿Qué atributos del nodo influyen en la efectividad de IpOpt?</li>
<li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" disabled=""> Tiempo ipopt</li>
</ul>
<hr>
<p><strong>Mecanismo para decidir cuando aplicar Ipopt</strong><br>
Tomar en cuenta tiempo y mejora (en %) de intervalo objetivo<br>
Vale la pena aplicar Ipopt cuando:</p>
<blockquote>
<ul>
<li>mejora considerablemente la calidad de la mejor solución</li>
<li>la mejora implica una reducción considerable en el tamaño del árbol de búsqueda (impacto de Y?)</li>
</ul>
</blockquote>
<p><strong>Comando para compilar</strong></p>
<pre><code>g++ -I/home/erick/ibex-lib/include/ibex/ -I/home/erick/ibex-lib/include/ibex/3rd -L/home/erick/ibex-lib/_build_/3rd/lib -std=c++11 -g -DNDEBUG -L/home/erick/ibex-lib/lib/ibex/3rd -L/home/erick/ibex-lib/lib /home/erick/ibex-lib/plugins/optim/main/ibexopt.cpp -Wl,--start-group -libex -lamplsolvers -lipopt -lgaol -lgdtoa -lultim -lsoplex -lz -ldl -Wl,--end-group -Wall -Wno-deprecated -Wno-unknown-pragmas -Wno-unused-variable -Wno-unused-function -Warray-bounds -v -o ibexopt -Wl,--rpath -Wl,/home/erick/CoinIpopt/lib -L/home/erick/CoinIpopt/lib -L/usr/lib/gcc/x86_64-linux-gnu/7 -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu -L/usr/lib/gcc/x86_64-linux-gnu/7/../../../../lib -L/lib/../lib -L/usr/lib/../lib -L/usr/lib/gcc/x86_64-linux-gnu/7/../../.. -llapack
</code></pre>
<h2 id="selección-dinámica-del-solucionador-local-baron">Selección dinámica del solucionador local (BARON)</h2>
<ol>
<li>
<p>Se asocia una tasa de éxito</p>
<ol>
<li>
<p>Para el límite superior (upper bounding), el solucionador local gana, si devuelve una solución que pasa la prueba de viabilidad y mejora el valor del límite superior conocido</p>
</li>
<li>
<p>Para el límite inferior, el solucionador local gana, si devuelve solución que satisface las <a href="http://apmonitor.com/me575/index.php/Main/KuhnTucker">condiciones KKT</a></p>
</li>
</ol>
</li>
<li>
<p>Para cada solucionador local, se guarda el número total de victorias en la rama, para (a) se denota <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>N</mi><mrow><mi>w</mi><mi>i</mi><mi>n</mi><mi>s</mi></mrow></msub></mrow><annotation encoding="application/x-tex">N_{wins}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: -0.10903em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight" style="margin-right: 0.02691em;">w</span><span class="mord mathdefault mtight">i</span><span class="mord mathdefault mtight">n</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span>  y para (b) el número de ganancias o pérdidas consecutivas  denotado por <span class="katex--inline"><span class="katex"><span class="katex-mathml"><math><semantics><mrow><msub><mi>N</mi><mrow><mi>c</mi><mi>o</mi><mi>n</mi><mi>s</mi><mi>e</mi><mi>c</mi><mi>u</mi><mi>t</mi><mi>i</mi><mi>v</mi><mi>a</mi><mi>s</mi></mrow></msub></mrow><annotation encoding="application/x-tex">N_{consecutivas}</annotation></semantics></math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height: 0.83333em; vertical-align: -0.15em;"></span><span class="mord"><span class="mord mathdefault" style="margin-right: 0.10903em;">N</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height: 0.311664em;"><span class="" style="top: -2.55em; margin-left: -0.10903em; margin-right: 0.05em;"><span class="pstrut" style="height: 2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight">o</span><span class="mord mathdefault mtight">n</span><span class="mord mathdefault mtight">s</span><span class="mord mathdefault mtight">e</span><span class="mord mathdefault mtight">c</span><span class="mord mathdefault mtight">u</span><span class="mord mathdefault mtight">t</span><span class="mord mathdefault mtight">i</span><span class="mord mathdefault mtight" style="margin-right: 0.03588em;">v</span><span class="mord mathdefault mtight">a</span><span class="mord mathdefault mtight">s</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height: 0.15em;"><span class=""></span></span></span></span></span></span></span></span></span></span> donde el número positivo indica número de victorias consecutivas, mientras que un número negativo denota derrotas consecutivas</p>
</li>
</ol>
<p>Además, si m victorias consecutivas , son seguidas por una pérdida , luego Nganancias se reestablece a cero.</p>
<p>Finalmente, definimos un rango rs ∈ [1 ,  r ] para cada solucionador s . En un nodo dado, los solucionadores se seleccionan para la búsqueda local en función de este rango. Un valor menor para el rango implica un mayor probabilidad de éxito. Inicializamos el rango de cada solucionador en función de nuestro conocimiento sobre el rendimiento promedio del solucionador en una gran cantidad de problemas de prueba, y se actualizará rs durante la búsqueda global . Si un solucionador falla η veces consecutivas, se disminuirá la frecuencia con que se llama al solucionador al degradar su rango -&gt; rs = min( 2rs ,  r) . Del mismo modo, si un solucionador gana η veces consecutivas, mejoramos su rango usando la relación rs = max ( 1 , rs/2 ) .</p>
<p>Antes de cada búsqueda local, empleamos el procedimiento de aprendizaje para seleccionar un solucionador local de la siguiente manera. Si todos los solucionadores locales han fallado muy a menudo, es decir, rs = r para todos los solucionadores, entonces el solucionador con el mayor número total de gana ( Nganados) está seleccionado; de lo contrario, se utiliza un solucionador con el mejor rango para buscar</p>
<h2 id="algoritmo-idea">Algoritmo (Idea)</h2>
<pre class=" language-python"><code class="prism  language-python"><span class="token comment">#factor (double) se setea en el main</span>
<span class="token builtin">int</span> T<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">;</span> <span class="token builtin">iter</span><span class="token operator">=</span><span class="token number">0</span>
<span class="token keyword">def</span> <span class="token function">upper_bounding</span><span class="token punctuation">(</span>box x<span class="token punctuation">,</span> loup<span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token builtin">iter</span> <span class="token operator">+=</span> <span class="token number">1</span>
	x <span class="token operator">=</span> default_finder<span class="token punctuation">(</span>x<span class="token punctuation">)</span> <span class="token comment">#midpoint + inHC4 + InnerTaylor</span>
	<span class="token keyword">if</span> f<span class="token punctuation">(</span>x<span class="token punctuation">)</span> <span class="token operator">&lt;</span> loup<span class="token punctuation">:</span> loup <span class="token operator">=</span> f<span class="token punctuation">(</span>x<span class="token punctuation">)</span>
	<span class="token keyword">if</span> <span class="token builtin">iter</span> <span class="token operator">%</span> T <span class="token operator">==</span> <span class="token number">0</span><span class="token punctuation">:</span>
 	    <span class="token comment">#calcular tiempo para obtener tiempo usado por IpOPt</span>
		x <span class="token operator">=</span> IpOpt<span class="token punctuation">(</span>x<span class="token punctuation">)</span> 
		<span class="token keyword">if</span> f<span class="token punctuation">(</span>x<span class="token punctuation">)</span> <span class="token operator">&lt;</span> loup<span class="token punctuation">:</span> 
		`  wins <span class="token operator">+=</span><span class="token number">1</span>
	   	   succesives <span class="token operator">+=</span> <span class="token number">1</span><span class="token punctuation">;</span> T<span class="token operator">/=</span> <span class="token punctuation">(</span>minimo T<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span>
		   loup <span class="token operator">=</span> f<span class="token punctuation">(</span>x<span class="token punctuation">)</span>
		<span class="token keyword">else</span><span class="token punctuation">:</span>
		   loses <span class="token operator">+=</span><span class="token number">1</span>
		   succesives <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span> T<span class="token operator">*=</span>
	<span class="token keyword">if</span> max_succesives<span class="token operator">&lt;</span>succesives<span class="token punctuation">:</span>
		max_succesives <span class="token operator">=</span> succesives
	<span class="token comment">#con T=1: en main imprimir max_succesives y wins/(wins+loses)</span>
</code></pre>

