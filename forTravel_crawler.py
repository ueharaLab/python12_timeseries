
import csv
import urllib.request
import urllib.parse
import urllib
import lxml.html
import time
import pymongo
	


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fortravelDB2024"]
reviews_collection = db['fortravel_reviews']

keyword=input('input keyword')
key_w = keyWord = urllib.parse.quote(keyword)



def scrape_review_detail(review_detail_root):

    review_detail_dic ={}
    #  <div class="u_tipsEachBox">    <h1 class="hdTitle" property="v:summary">ハイアット リージェンシー 京都</h1>
    title = review_detail_root.xpath("//h1[@class='hdTitle']")
    if len(title)!=0:
        title_text=title[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
        #print('title',title_text)
        review_detail_dic['title']=title_text
    
    # <p property="v:description"
    body_path = review_detail_root.xpath("//p[@property='v:description']")
    if len(body_path)!=0:
        body_txt =body_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')[0:4999]
        #print('body',body_txt)
        review_detail_dic['body']=body_txt
    
            
    #<span class="postedStar star50_l %>" property="v:rating"> 5.0
    total_eval_path = review_detail_root.xpath("//span[@property='v:rating']")
    if len(total_eval_path)!=0:
        total_eval = total_eval_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
        #print('total_eval',total_eval)
        review_detail_dic['total_eval']=total_eval
        
    
    #<div class="u_tipsSatisfiedItem">
    #<dl class="group">
    #<dt>アクセス</dt>
    #<dd class="rankTotal"><span class="star50_s">5.0</span></dd>
    #</dl>
    detail_eval_path = review_detail_root.xpath("//div[@class='u_tipsSatisfiedItem']")
    if len(detail_eval_path)!=0:
        detail_evals = {}
        node= detail_eval_path[0]
        detail_path = node.xpath(".//dl[@class='group']")
        for dp in detail_path:
            detail_eval = dp.text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
            #print(detail_eval)
            detail_eval_dic = detail_eval.split('：')
            if len(detail_eval_dic)==2:
                detail_evals[detail_eval_dic[0]] = detail_eval_dic[1]
        #print(detail_evals)
        review_detail_dic['detail_evaluation']=detail_evals    

    #<p class="postDay">クチコミ投稿日:2024/05/26</p>
    #<p content="2024/07/14" property="v:dtreviewed" class="tipPostedDay">クチコミ投稿日：2024/07/14</p>

    post_date_path = review_detail_root.xpath("//p[@class='tipPostedDay']")
    if len(post_date_path)!=0:
        post_date = post_date_path[0].text_content().replace('\r\n','').replace('\n','').replace('<br />','').replace(' ','')
        #print('post_date',post_date)
        review_detail_dic['post_date']=post_date
    
    
    '''
    p class="clipImageInner">
          <a rel="nofollow" class="clipImage img_liquid_area" data-lightbox="group" href="http://cdn.4travel.jp/img/tcs/t/tips/pict/src/197/370/src_19737091.jpg?1721056618">
              <img alt="ホテル写真" style="display:none" src="https://cdn.4travel.jp/img/thumbnails/imk/tips_pict/19/73/70/200x200_19737091.jpg" />
    '''
    pic_path = review_detail_root.xpath("//p[@class='clipImageInner']/a/img")
    if len(pic_path)!=0:
        pic_link=[]
        for p in pic_path:
            pic_link.append(p.get('src'))
        #print(pic_link)
        review_detail_dic['pic_link']=pic_link


    return review_detail_dic






page=0
review_scraped=[]


while True:

    

    page = page +1
    time.sleep(1)
    print(page)
   
    html = urllib.request.urlopen(' https://4travel.jp/search/review/dm?order=desc&page={0}&sa={1}&sort=visited_at'.format(page,key_w)).read() 
     
    root = lxml.html.fromstring(html.decode('utf-8',errors='replace'))
    # <p class="summary_ttl">
    #    <a class="tips_cs4_5_l" href=
    
    
    if page % 10 ==0:
        print(review_scraped)
        reviews_collection.insert_many(review_scraped)
        review_scraped=[]
    
       
    
    
    #review_list = root.xpath("//p[@class='summary_ttl']/a") <li class="">	
    review_list = root.xpath('//li[@class=""]')	
    for review in review_list:	

        review_path = review.xpath(".//p[@class='summary_ttl']/a")
        href =review_path[0].get('href')
        
        #for rvw in review_path:
        #url = rvw.get('href')
            
       
        review_pageHtml = urllib.request.urlopen(href).read()       		
        review_detail_root= lxml.html.fromstring(review_pageHtml.decode('utf-8'))        
        review_dic = scrape_review_detail(review_detail_root)    
        

        '''
        <div class="spot_box">
              <p class="spot_name spot_hotel_m">
                <a href="https://4travel.jp/dm_hotel-11994549">アパホテル 京都五条大宮</a>
              </p>
              <p class="spot_info">
                エリア：京都駅周辺 (京都)

            <br>
                カテゴリー：
                  宿・ホテル
                  
        '''
        
        if len(review_dic)!=0:
            spot_path = review.xpath(".//div[@class='spot_box']/p/a")
            if len(spot_path)!=0:
                spot_name = spot_path[0].text_content()                
                spot_link = spot_path[0].get('href')
                review_dic['spot_name']=spot_name
                review_dic['spot_link']=spot_link
            
            spot_info_path = review.xpath(".//p[@class='spot_info']")
            if len(spot_info_path)!=0:
                spot_info = spot_info_path[0].text_content()
                review_dic['spot_info']=spot_info







        #print(review_dic)
        review_scraped.append(review_dic)
        