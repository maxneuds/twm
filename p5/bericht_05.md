# TWM, Praktikumsbericht 5

Gruppe ZA: Denis Fedjakin, Maximilian Neudert

---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>

## Teil I

### 1.

Wir schauen uns 10 zufällige Daten aus dem Trainingsset an:

```bash
0: ? this was not enjoyable to watch...
0: ? boring stuff we got here...
1: ? the first review i saw of page 3 said what is ? ? finally wants to say should he say something so ? br br the most beautiful thing about page 3 is it doesn't take sides no propaganda whatsoever this is the film that captures so many angles of an issue i don't know what do i call as an issue here and yet like any mediocre movie doesn't come up with an solution i was so intrigued when i realized that the movie ended almost in the same scenario just like it started br br the movie ? so many characters who are completely with completely different ? and different ? and yet they are all a part of the system which is all the more ? i wish i can say more but there would be more spoilers ahead so watch page 3 if you wanna see one of the most mature films of the recent times
1: ? more than twenty years before peter jackson's ? adaptation of the lord of the rings there was this 1978 animated effort from director ralph bakshi an ambitious and reasonably faithful version of the story this has sadly been rather over ? by the jackson trilogy indeed many reviewers here on the imdb mainly those who saw the newer version first seem to be ? ? to this version but if one applies a little common sense and takes into consideration the time when it was made and the technical possibilities that existed at that time then they will realise that this is a pretty good film indeed it was shortly after seeing this animated movie back in the early '80s that i sought out ? book and immediately became a ? fan of these richly detailed middle earth adventures so in some respects i owe this film a degree of ? as the film which shaped my literary tastes forever br br ? the dark lord of middle earth ? an all powerful ring that gives him incredible power following a great battle during which ? is defeated the ring falls into possession of a king named ? but instead of destroying it he ? chooses to keep it for centuries the ring passes from hand to hand eventually coming into the possession of a ? named ? ? who lives in a peace loving community known as the ? ? learns from a wizard named ? that his ring is in fact the one ring the very same that was ? by ? all those centuries ago and that its master is once again searching for it in order to ? his dark power over the entire land ? ? on a ? journey to protect the ring with three other ? companions but every step of the way they are hunted by ? ring ? the black riders there follow many adventures during which a company of nine ? is formed to guide the ring to the only place where it can be ?  ? doom in the land of ? the film concludes with ? and his best friend sam on the borders of ? closing ever ? to their horrifying destination meanwhile ? and the other members of the company fight off a huge army of ? at the legendary ? of ? deep br br this version covers just over half of the original book a second ? was planned to bring the story to an end but was sadly never completed while the ending feels abrupt it does at least end at a sensible point in the story one has to feel a little frustration and regret that no sequel exists in which we might follow these animated heroes to their eventual goal the animation is passable with a nice variety of locales and characters presented in interesting detail the music by leonard ? is suitably stirring and fits in appropriately with
0: ? straight to the point the groove tube is one of the most unfunny ? and downright horrible films ever made ...
```

Den Labels stimmen wir zu.
Die negativen Labels sind meist sehr schnell sehr klar und dafür gibt es oft starke Keywords. Positive labels sind schwieriger, da dort Filme auch gerne mal mehr beschrieben werden.

### 2.

Wir erhalten als 20 relevanteste features:

| index | feature   |
| ----- | --------- |
| 463   | and       |
| 758   | awful     |
| 788   | bad       |
| 961   | best      |
| 1116  | boring    |
| 3141  | excellent |
| 3919  | great     |
| 4213  | his       |
| 4291  | horrible  |
| 4841  | just      |
| 5276  | love      |
| 5785  | movie     |
| 5961  | no        |
| 6005  | nothing   |
| 8440  | stupid    |
| 8737  | terrible  |
| 9468  | waste     |
| 9652  | wonderful |
| 9683  | worse     |
| 9685  | worst     |

### 3.

Accuracy ist dann kritisch, wenn die Anzahl an Labels im Datensatz stark asymmetrisch verteilt sind, da dann dumme einseitige Klassifizierungen zu einer hohen Genauigkeit führen.
Der vorliegende Datensatz ist aber stark symmetrisch, sprich es sind etwa gleich viele Daten von jedem Label vorhanden und somit ist Accuracy ein gutes Maß.

Im Testdatensatz sind 25'000 Datenpunkte und dies bedeutet, dass eine Abweichung einen prozentualen Feher von `0.004%` ausmacht.
Das ist sehr wenig und bedeutet, dass wenn die Accuracy nicht besonders hoch ist man diese als Gütemaß verwenden kann, aber wenn es nu um wenige Abweichungen geht, sprich sagen wir mal die Modelle unterscheiden sich um 100 Abweichungen, dann wären das gerade mal `0.4%` also kaum sichtbar im Gütemaß.
Zusätzlich ist der

### 4.

Etwa ab der 4. Epoche laufen Training- und Validierungsaccuracy auseinander, das heißt der Algorithmus fängt mit overfitting an. Sprich man sollte nicht mehr als 4 Epochen trainieren.

### 5.

- FP: Das Modell wird stark dadurch verwirrt, dass im Review der Film differenziert betrachtet wird also "mir hat der Film nicht gefallen trotz des sehr guten..." oder durch Ironie oder Troll-Bewertungen.
- FN: Hier fällt auf, dass die Bewertungen sehr lang sind auch die Filme auch differenziert betrachtet werden.

### 6.

Man sieht, dass selbst nach 10 Epochen Validation Accuracy etwa bei 50% liegt, sprich der Algorithmus rät und die Training Accuracy ist auch etwa auf diesem Niveau, aber man erkennt einen konkaven Verlauf.
Dies wird wohl daran liegen, dass mit vortrainierten Gewichten trainiert wird und diese können auf einem Datensatz mit komplett anderen Labels basieren. Der Kontext des vortrainierten Datensatzes ist nicht bekannt und es kann duchaus sein, dass die Worte dort im Zusammenhang andere Bedeutung haben, als im aktuellen Zusammenhang. Und wenn die Lernrate entsprechend klein ist, dann tut sich da innerhalb von 10 Epochen auch nicht viel.

### 7.

Es wird erwartet, dass das Training weniger schnell ins Overfitting läuft und oszillieren im Validation Loss durch den Memory Effekt unterdrückt wird. Dies ist auch der Fall.

### 8.

Wir erwarten, dass die einfachen Modelle deutlich schlechtere Ergebnisse liefern.
Die logistische Regression liefert überraschend gute Ergebnisse. Die Bedeutung der Keywords ist hierbei nicht so stark, da durch die logistische Regression auch entsprechend stark geglätted wird. Hier ist insbesondere schön, dass die Wörter durch den Algorithmus auf natürliche Weise in positive (Gewicht nahe 0) und negative Wörter (Gewicht nahe 1) getrennt werden.
Der Decision Tree liefert ein deutlich schlechteres Ergebnis, da dieser die Keywords stärker ins Gewicht nimmt und insbesondere mit denen Overfitting verursacht, da die Anzahl an Keys im Baum gar nicht mal so groß ist.
