---


---

<h1 id="todo">TODO</h1>
<ul>
<li>Estudiar C++. <a href="https://dis.unal.edu.co/~fgonza/courses/2003/poo/c++.htm">link clase ejemplo</a>, <a href="http://www.cplusplus.com/reference/list/list/">documentación c++</a></li>
<li>Estudiar bien el problema (set union knapsack).</li>
<li>Buscar instancias de prueba y benchmarks.</li>
<li>Proponer la organización de los datos.</li>
<li>Tratar de leer archivos de entrada y guardarlos dentro del problema.</li>
</ul>
<h1 id="idea">Idea</h1>
<p>Inspirado en:<br>
<a href="https://sci-hub.se/10.1016/j.future.2019.07.062">Iterated two-phase local search for the Set-Union Knapsack Problem</a></p>
<p>Algoritmo que mantiene la “esencia” del paper.</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">solve</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
   random_greedy<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment">#construcción de solución inicial</span>
   <span class="token keyword">while</span> time <span class="token operator">&lt;</span> time_limit
      local_search<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment"># e.g., hill climbing o SA para mejorar resultados</span>
      perturbation<span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token comment"># or random_greedy()</span>
</code></pre>
<p>El <code>random_greedy</code> básicamente coloca los items uno a uno en la mochila. En el paper usan un greedy determinista. Yo lo haría aleatorio (e.g, escoger uno de los mejores en vez del mejor).</p>
<p><img src="https://i.imgur.com/ZCPDunx.png" alt="image"></p>
<p>Para la <code>local search</code> se podría implementar un algoritmo que vaya haciendo swaps aleatorios y vaya aceptando sólo aquellos que mejoran la función objetivo (hill climbing). En el paper proponen estos movimientos. Yo me quedaría sólo con el primero. Generalmente, el algoritmo debería detenerse luego de un número consecutivo de swap fallidos (50?)</p>
<p><img src="https://i.imgur.com/B5CNEqK.png" alt="image"></p>
<p>Para la <code>perturbation</code>, en el paper sacan algunos elementos de la mochila y colocan otros aleatoriamente hasta que la capacidad lo permita. El objetivo de esto es “comenzar” a buscar de nuevo con una solución <em>parecida</em> a la mejor encontrada previamente.</p>
<p>Otra opción es comenzar de cero haciendo un <code>random_greedy</code>.</p>
<h2 id="¿y-dónde-colocamos-aprendizaje">¿Y dónde colocamos aprendizaje?</h2>
<p>Se me ocurre lo siguiente. Mantener una lista con las soluciones/estados retornados por la búsqueda local.<br>
En cada iteración debemos decidir si perturbamos un estado en el conjunto L, o si partimos de uno nuevo (<code>random_greedy</code>)</p>
<pre class=" language-python"><code class="prism  language-python"><span class="token keyword">def</span> <span class="token function">solve</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
   S <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
   <span class="token keyword">while</span> time <span class="token operator">&lt;</span> time_limit
      s <span class="token operator">=</span> select a state <span class="token keyword">from</span> S 
	         <span class="token operator">or</span> create a new state <span class="token keyword">with</span> random_greedy 
      s' <span class="token operator">=</span> local_search<span class="token punctuation">(</span>s<span class="token punctuation">)</span>  
      <span class="token keyword">if</span> f<span class="token punctuation">(</span>s'<span class="token punctuation">)</span> <span class="token operator">&gt;</span> Sb<span class="token punctuation">:</span> 
         Sb <span class="token operator">=</span> f<span class="token punctuation">(</span>s'<span class="token punctuation">)</span> <span class="token comment">#se actualiza mejor solución</span>
      s<span class="token string">' = perturbate(s'</span><span class="token punctuation">)</span>
      S<span class="token punctuation">.</span>add<span class="token punctuation">(</span>s'<span class="token punctuation">)</span>
</code></pre>
<p>Cada estado en <code>S</code> puede almacenar la siguiente información:</p>
<ul>
<li>Mejor solución encontrada a partir del estado (o máximo f(local_search(s) - f(s) ) )</li>
<li>Promedio/desviación estándar de evaluaciones a partir del estado</li>
<li>Número de veces que el estado ha sido seleccionado</li>
<li>Otra información relacionada con el problema</li>
</ul>
<p>Y a partir de esta información nos interesa identificar el estado con mayor probabilidad de mejorar el <code>Sb</code>.</p>
<p>Para entrenar el asunto, se puede correr el algoritmo 100 veces con cada diferente estado de partida. Luego se ordenan las soluciones encontradas (sol) de peor a mejor y vamos creando muestras.</p>
<p>Información del estado s + f(sol_i)  --&gt;  100-i%<br>
Es decir hay un 100-i% de probabilidad de que el estado s produzca una solución mejor a sol_i.</p>

