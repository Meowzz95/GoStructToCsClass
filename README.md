# GoStructToCsClass
Use this when you are writting a .net core application that needs a model from Go project.

Simply copy your go struct in `input.txt`, run `main.py`, you will get .net core class with `JsonProperty` set.

# This is a not a production ready project
I just use it for my own convenience, however you can benifit from it if you are in similar situlation :)

# Example

input.txt

```go
type GoFantasticClass struct{
	FantasticId              string     `json:"fantasticId" bson:"fantasticId" form:"fantasticId"`
	Items                    []Item     `json:"items" bson:"items" form:"items"`
	IsBest                   int        `json:"isBest" bson:"isBest" form:"isBest"`
	Author                   string     `json:"author" bson:"author" form:"author"`
	Whatever                 bool       `json:"whatever" bson:"whatever" form:"whatever"`
}
```

out/GoFantasticClass.cs
```cs
public class GoFantasticClass
{
    [JsonProperty(PropertyName = "fantasticId")]
    public string FantasticId { get; set; }

    [JsonProperty(PropertyName = "items")]
    public Item[] Items { get; set; }

    [JsonProperty(PropertyName = "isBest")]
    public int IsBest { get; set; }

    [JsonProperty(PropertyName = "author")]
    public string Author { get; set; }

    [JsonProperty(PropertyName = "whatever")]
    public bool Whatever { get; set; }

}

```
