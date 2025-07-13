from ext import app, db
from models import Article, Feedback, User, Category

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="123", role="admin")
    admin.create()

    Mariam = User(username = "mariam", password="Mariami123", profile_pic="asd.jpg")
    Mariam.create()

    STEM = Category(Name = "STEM", image="STEM.jpg", Link="/category/STEM",
        Description = "Explore science, technology, engineering, and math with practical insights and creative problem-solving.")
    STEM.create()

    Literature = Category(Name = "Literature", image="lit.jpg", Link="/category/Literature",
        Description = "Dive into storytelling, analysis, and the power of words—from classics to contemporary.")
    Literature.create()

    Brontes = Article(category = "Literature", heading = "The Brontë Sisters", description = "A look at how Charlotte, Emily, and Anne Brontë defied expectations to write some of the boldest novels of their time.",
                      summary = "Among the moors and melancholy of 19th-century England, the Brontë sisters defied societal norms and expectations to become literary legends. Their stories were daring, emotional, and unforgettable.",
                      Subheading1 = "Early Life in Isolation", 
                      text1 = "Growing up in the remote village of Haworth, the sisters were surrounded by bleak landscapes and a strict upbringing. Their imaginations bloomed in isolation, crafting detailed fantasy worlds that laid the foundation for their novels.",
                      
                      Subheading2 = "Pseudonyms and Publishing", 
                      text2 = "To navigate the male-dominated literary world, they published under male pen names: Currer, Ellis, and Acton Bell. This decision wasn’t just about acceptance—it was survival.",
                      
                      Subheading3 = "Defying Victorian Expectations", 
                      text3 = "Charlotte’s Jane Eyre, Emily’s Wuthering Heights, and Anne’s The Tenant of Wildfell Hall each challenged the norms of romance, morality, and feminine obedience. These were not delicate love stories—they were fierce declarations of agency.",
                      
                      Subheading4 = "A Brief Flame", 
                      text4 = "Despite their brilliance, the sisters' lives were tragically short. Yet their impact has lasted centuries, inspiring generations to write boldly.",
                      
                      image = "article1.JPG")
    Brontes.create()

    Marie = Article(category = "STEM", heading = "Marie Curie", description = "The story of the first person to win two Nobel Prizes—and the risks she took to change science forever.",
                      summary = "Marie Curie wasn’t just the first woman to win a Nobel Prize—she was the first person to win two. Her scientific brilliance changed the world, even as it quietly destroyed her health.",
                      Subheading1 = "Breaking Through Barriers", 
                      text1 = "Born in Poland and denied education as a woman, Curie moved to Paris and entered the Sorbonne, becoming a standout in her field.",
                      
                      Subheading2 = "The Discovery of Radium and Polonium", 
                      text2 = "Curie and her husband Pierre isolated new radioactive elements, a discovery that would later be used in medicine and warfare. Their lab work was painstaking and dangerous.",
                      
                      Subheading3 = "A Legacy of Firsts", 
                      text3 = "Marie was the first woman to win a Nobel, the first to teach at the Sorbonne, and the first to lie in the Panthéon on her own merit. She opened doors by simply refusing to let them stay closed.",
                      
                      Subheading4 = "The Cost of Curiosity", 
                      text4 = "She carried test tubes in her pockets, touched radioactive material daily, and had no idea of the risks. Her eventual death from exposure is a reminder of the sacrifices that come with discovery.",
                      
                      image = "STEM.jpg")
    Marie.create()