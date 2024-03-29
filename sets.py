from enums import ConnectionType, Side, TileFeatureAttribute
from tile import TileSet, Tile
from feature import TileCity, TileRoad, TileMonastery, TileFarm

# reusable tile features
monastery = TileMonastery()

# cities
city_cap_right = TileCity([Side.RIGHT])
vertical_tunnel_city = TileCity([Side.TOP, Side.BOTTOM])

# roads
vertical_road = TileRoad([Side.TOP, Side.BOTTOM])
feature_entrance = TileRoad([Side.CENTER, Side.BOTTOM])


base_set = TileSet("base", 
    {Tile("monastery_road", ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.ROAD, ConnectionType.GRASS,
        roads = [feature_entrance],
        monastery = monastery,
        farms = [TileFarm([Side.TOPLEFT, Side.TOPRIGHT, Side.BOTTOMRIGHT, Side.BOTTOMLEFT])]): 2, 
        
    Tile("monastery", ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.GRASS,
        monastery = monastery,
        farms = [TileFarm([Side.TOPRIGHT, Side.BOTTOMRIGHT, Side.BOTTOMLEFT, Side.TOPLEFT])]): 4,

    Tile("big_city", ConnectionType.CITY, ConnectionType.CITY, ConnectionType.CITY, ConnectionType.CITY,
        cities = [TileCity([Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT], [TileFeatureAttribute.SHIELD])]): 0,

    Tile("city_cap_straight_road", ConnectionType.ROAD, ConnectionType.CITY, ConnectionType.ROAD, ConnectionType.GRASS,
        cities = [city_cap_right],
        roads = [vertical_road],
        farms = [TileFarm([Side.TOPLEFT, Side.BOTTOMLEFT]), TileFarm([Side.TOPRIGHTTOP, Side.BOTTOMRIGHTBOTTOM], adjacent_cities = {city_cap_right})]): 3,

    Tile("city_tunnel", ConnectionType.CITY, ConnectionType.GRASS, ConnectionType.CITY, ConnectionType.GRASS,
        cities = [vertical_tunnel_city],
        farms = [TileFarm([Side.TOPLEFTLEFT, Side.BOTTOMLEFTLEFT], adjacent_cities = {vertical_tunnel_city}), TileFarm([Side.TOPRIGHTRIGHT, Side.BOTTOMRIGHTRIGHT], adjacent_cities = {vertical_tunnel_city})]): 1,

    Tile("tri_road", ConnectionType.GRASS, ConnectionType.ROAD, ConnectionType.ROAD, ConnectionType.ROAD,
        roads = [TileRoad([Side.CENTER, Side.RIGHT]), TileRoad([Side.CENTER, Side.BOTTOM]), TileRoad([Side.CENTER, Side.LEFT])],
        farms = [TileFarm([Side.TOPLEFT, Side.TOPRIGHT]), TileFarm([Side.BOTTOMRIGHT]), TileFarm([Side.BOTTOMLEFT])]): 4,
    }, 
    
    Tile("start", ConnectionType.ROAD, ConnectionType.CITY, ConnectionType.ROAD, ConnectionType.GRASS,
        cities = [city_cap_right],
        roads = [vertical_road],
        farms = [TileFarm([Side.TOPLEFT, Side.BOTTOMLEFT]), TileFarm([Side.TOPRIGHTTOP, Side.BOTTOMRIGHTBOTTOM], adjacent_cities = {city_cap_right})]))