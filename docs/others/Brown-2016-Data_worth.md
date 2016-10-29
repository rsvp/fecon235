## How Much Is Your Data Worth? (edited excerpt)

by Rich Brown, 24 Oct 2016, [Original version](https://www.linkedin.com/pulse/how-much-your-data-worth-rich-brown)

Big banks and hedge funds make billions from trading and investing with data, 
and you’ve got some of the most unique alternative data on the market. 
So why shouldn’t you get millions of dollars per customer for your data? 
Well, the answer may not be that straightforward, but 
here are some factors that may help you in developing your case. 

### Predictive Properties

The million-dollar question and the one that trumps just about everything else 
is *whether your data set has predictive powers for the market*. 
You’ll need to know if it can predict something specific about financial markets 
(volume, volatility, returns) – and ideally back that up with proof. 
You will want to understand how to use it, what it does, when it works, when it doesn’t, 
what it is correlated with and what it contradicts, its Sharpe ratio, and 
its alpha (excess return over the market and other factors). 
As you look at the potential use cases, consider the following:

- **Trading vs Investing** - As you approach the exercise, it is important to 
put your data in the context of how it is likely to be used. 
More precisely, is this a fast-moving data set likely to drive trading behavior 
(sub-second to days of position holding), or is it an infrequently updated data set 
likely to be used to understand trends over time and drive investment use cases 
(weeks to months or longer of position holding)?
    
- **Historical Depth of Data** - The simple rule here is that the 
longer one expects the data to influence investment decisions, the longer the history you need. 
Trading use cases can usually be served with two years or less of data (assuming there are ample 
tradable events within that history to validate the data’s value, consistency, frequency, etc.). 
Investment data sets will often require far more than two years of history, 
sometimes needing to span multiple economic cycles.  

- **Macro vs Micro** - Similar to the trading vs investing use case, 
does your data likely drive macro or microstructure value/decisions. 
For example, is your data stock or instrument specific (microstructure in nature) 
or is it telling of a larger macro trend like US GDP or consumer confidence? 
In the former, there are many ways to both trade and invest and the 
timings of such plays can vary. In the latter case, there are also many 
ways to play this out, but because of the interconnected markets, 
once the primary trigger begins to move, the second-degree effects begin 
to take hold and your data may not be needed for those opportunities to be realized.

- **Liquidity Considerations** - If you get past the predictive argument in your data, 
you still need to understand if there is enough liquidity in those trades – 
both to enter the position, and more importantly due to higher risk, to exit the position. 
If one can not capture the alpha your data shows that it can generate, 
it is of significantly less practical use.

Aside from direct market correlations, consider also whether it can predict 
something else that quant firms are already using in their models 
(e.g. consumer confidence, interest rate movements). 
Predicting these events/signals may provide a quicker way to capitalize on the 
opportunities in front of you. While your original studies in this realm 
may be somewhat limited, it can guide your sales team on who to target, 
how to position the data, and how to help clients test the data. 

### Exclusivity

Exclusivity tends to be a double-edged sword when it comes to how broadly 
you offer your data set and the premium you may be able to command. 
Too many clients and your data’s value may likely erode. 
Too few clients and you may attract regulatory and media scrutiny, 
neither of which your prospects are keen on facing. 

Your data is not likely the only game in town. 
Direct substitutes may include data from other geolocation services, 
and may be numerous in nature (consider all of the apps on your phone that 
likely track your location). Also, while you may have the largest collection 
of consumer location data on the planet, a competitor offering a much 
smaller sampling may be able to generate the same value, and do it at a cheaper cost. 
This will decrease the premium you may command for your service, so 
consider focusing on making the product more usable as a differentiator.

Indirect substitutes can also undermine the value of your data set. 
Satellite imagery, credit/debit card purchase history, and even *aggregations* 
of your raw data may provide additional proxies for same store sales and thus 
reasonable alternatives to your offering. So don’t be too boastful about 
how special your data is or too greedy when it comes to pricing.

### Complexity and Product Variants 

Complicated data sets that can not be easily explained or consumed 
without significant subject matter expertise make it harder for your prospects to test. 
It will consume more resources on their side, lengthen your sales cycle, 
and limit the scale of your reach. In the case of location-based intelligence on consumers 
(a potential proxy for same store sales), billions of location data points per day 
in latitude/longitude format might be a hard for the average hedge fund to consume, 
even by those with geospatial analytic expertise. Instead, consider mapping the 
lat/lon coordinates to store locations and offer your service as a number of 
visits per store per day/week/month or normalize data in several other ways. 

While you may be able to capture premiums from those firms that have the 
ability and willingness to pay for your “fire hose” of data, you may be missing 
quite a large segment of the market and should consider offering variants 
of your product which could include store chain reports, sector or sub-sector 
level offerings. You may also want to account for your audience and 
adjust your data snapshots to suit specific behaviors. 
For instance, futures traders are more interested in underlying commodity behavior 
and may look at all meat-serving restaurant sales to predict cattle futures, while an 
equities trader may be more interested in a specific publicly traded food service company.

### Content Consistency 

Does the data look the same and act the same over time? 
If your analytic models have evolved over time or 
if you’ve added significant features such as new fields and ontologies, 
it is important that you have a true Point-In-Time representation of the data. 
More aptly, at the time the data was published, what did you know about it or 
what would you have known about it if your models in their current state existed back then? 
This may often mean rescoring the entire history so the historical data looks like 
how it would have been scored had those advancements been available at the 
time of content creation. You will also need a versioning of your data set 
along with a robust data dictionary of how those changes occurred over time. 
This also helps minimize *look-ahead bias* when evaluating your data set. 

Do not underestimate the importance of good documentation! 
Well documented data includes any relevant indexing by time, descriptions on how the data has 
changed over time, what the metadata fields mean, how it is assembled, any adjustments 
that are made, frequently asked questions, back-testing results showcasing 
how you performed the studies, etc. This will help ensure your data is 
interpreted correctly, speed up the evaluation, and reduce your overall support burden.

