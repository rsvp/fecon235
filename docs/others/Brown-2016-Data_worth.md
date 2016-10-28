## How Much Is Your Data Worth?

by Rich Brown, 24 Oct 2016 [Original version](https://www.linkedin.com/pulse/how-much-your-data-worth-rich-brown)

Big banks and hedge funds make billions from trading and investing with data, 
and you’ve got some of the most unique, sought after alternative data on the market. 
So why shouldn’t you get millions of dollars per customer for your data? 
Well, the answer may not be that straightforward, but 
here are some factors that may help you in developing your case. 

### Predictive Properties

The million-dollar question and the one that trumps just about everything else 
is *whether your data set has predictive powers for the market*. 
You’ll need to know if it can predict something specific about financial markets 
(volume, volatility, returns) – and ideally back that up with proof. 
You will want to understand how to use it, what it does, when it works, when it doesn’t, 
what it is correlated with and what it contradicts, its Sharpe ratio, and, of course, 
its alpha (what it generates in excess return over the market and other factors). 
As you look at the potential use cases, consider the following:

- **Trading vs Investing** - As you approach the exercise, it is important to 
put your data in the context of how it is likely to be used. 
More precisely, is this a fast-moving data set likely to drive trading behavior 
(sub-second to days of position holding), or is it an infrequently updated data set 
likely to be used to understand trends over time and drive investment use cases 
(weeks to months or longer of position holding)?
    
- **Macro vs Micro** - Similar to the trading vs investing use case, 
does your data likely drive macro or microstructure value/decisions. 
For example, is your data stock or instrument specific (microstructure in nature) 
or is it telling of a larger macro trend like US GDP or consumer confidence? 
In the former, there are many ways to both trade and invest and the 
timings of such plays can vary. In the latter case, there are also many 
ways to play this out, but because of the interconnected markets, 
once the primary trigger begins to move, the second-degree effects begin 
to take hold and your data may not be needed for those opportunities to be realized.

- **Liquidity Considerations** – If you get past the predictive argument in your data, 
you still need to understand if there is enough liquidity in those trades – 
both to enter the position, and more importantly due to higher risk, to exit the position. 
If one can not capture the alpha your data shows that it can generate, 
it is of significantly less practical use.

Aside from direct market correlations, consider also whether it can predict 
something else that quant firms are already using in their models 
(broker recommendations, consumer confidence, interest rate movements, etc.). 
Predicting these events/signals may provide a quicker way to capitalize on the 
opportunities in front of you. And, while your original studies in this realm 
may be somewhat limited, it can guide your sales team on who to target, 
how to position the data, how to help clients test the data, 
and can even influence the product roadmap. 

### Exclusivity

Exclusivity tends to be a double-edged sword when it comes to how broadly 
you offer your data set and the premium you may be able to command. 
Too many clients and your data’s value may likely erode. 
To few clients and you may attract regulatory and media scrutiny, 
neither of which your prospects are keen on facing. 

**Threat of Substitutes** – Flipping the exclusivity argument around, 
as in any competitive industry, your data is not likely the only game in town. 
Even if you have some sort of exclusive relationship with the data, 
you need to consider substitutes in both the direct and indirect sense. 
Direct substitutes may include data from other geolocation services data, 
and may be numerous in nature (consider all of the apps on your phone that 
likely track your location). Also, whilst you may have the largest collection 
of consumer location data on the planet, a competitor offering a much 
smaller sampling may be able to generate the same value, and do it at a cheaper cost. 
This will decrease the premium you may command for your service, so 
consider focusing on making the product more usable as a differentiator.  
Indirect substitutes can also undermine the value of your data set. 
Satellite imagery, credit/debit card purchase history, and even *aggregations* 
of your raw data (stores, sectors, even time/update frequency variants) 
may provide additional proxies for same store sales and thus reasonable 
alternatives to your offering. So, don’t be too boastful about 
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
level offerings (quick service restaurants or consumer electronic stores), or 
you may also want to account for your audience and adjust your data 
snapshots to suit specific behaviors. 
For instance, futures traders are more interested in underlying commodity behavior 
and may look at all meat-serving restaurant sales to predict cattle futures, while an 
equities trader may be more interested in a specific publicly traded food service company.

**Historical Depth of Data** – The simple rule here is that the 
longer one expects the data to influence investment decisions, the longer the history you need. 
Trading use cases can usually be served with two years or less of data (assuming there are ample 
tradable events within that history to validate the data’s value, consistency, frequency, etc.). 
Investment data sets will often require far more than two years’ history, 
sometimes needing to span multiple economic cycles.  

### Content Consistency 

Does the data look the same and act the same over time? 
If your analytic models have evolved over time (this is natural as you get smarter) or 
if you’ve added significant features such as new fields and ontologies, 
it is important that you have a true Point-In-Time representation of the data. 
More aptly, at the time the data was published, what did you know about it or 
what would you have known about it if your models in their current state existed back then? 
This may often mean rescoring the entire history so the historical data looks like 
how it would have been scored had those advancements been available at the 
time of content creation. You will also need a versioning of your data set 
along with a robust data dictionary of how those changes occurred over time. 
This also helps minimize the look-ahead bias when evaluating your data set. 

**Usability** can take many forms from whether it is standardized/normalized to 
whether or not it can be easily consumed.

- Timestamps – Does the data have timestamps that are consistent and synchronized over time? 
    
- Format – Is the data in a consistent format (HTML, CSV, JSON, etc.) that is easily consumed 
by the popular analytic tools?

- Size – How large is the data set and how has the volume changed over time? 
Abnormal growth rates, acquisition-driven spikes in data, massive content collection efforts, 
etc. all bode well for long-term value creation, but they do make it more difficult to 
use in the short-term, particularly if the reasons for such anomalous growth can 
not be easily explained or normalized. As mentioned in the complexity section, 
consider data aggregations which may remove unnecessary data that won’t likely be used.

- Accessibility – How easily can potential clients get access to the data? 
Hundred-terabyte data sets that have to be burned to disk can consume significant internal 
resources to produce and support. Consider hosting in the cloud or offering it via a 
cross-connect within the major trading locations, the latter being particularly relevant 
for high-speed trading use cases.  

- Documentation – Do not underestimate the importance of good documentation! 
Well documented data includes any relevant indexing by time, descriptions on how the data has 
changed over time, what the metadata fields mean, how it is assembled, any adjustments 
that are made, frequently asked questions, back-testing results showcasing 
how you performed the studies, etc. This will help ensure your data is 
interpreted correctly, speed up the evaluation, and reduce your overall support burden.

- Referential data – Does your data include referential or supplemental data likely to be 
used by most of your clients? This may include normalizing the data to a ticker level, 
mapping people or products to companies, lat/lon coordinates to company site locations, etc. 
Note the importance of Point-In-Time here as well. 
Companies merge, locations have retail site turnover, etc., and this can affect the results.

As you can see, many factors affect the valuation of your data set 
and the level of resource commitment you will need to effectively make it a compelling offering. 
Understanding the appropriate trade-offs can help you better position your data in the market, 
understand your resource requirements, set the product roadmap and support infrastructure, 
choose the right go-to-market strategy, and perhaps, monetize it at the appropriate time and pace. 

