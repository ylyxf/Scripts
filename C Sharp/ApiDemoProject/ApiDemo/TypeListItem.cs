using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ApiDemo
{
    public class TypeListItem
    {
        public TypeListItem(Type t)
        {
            this.Type = t;
        }

        public Type Type { get; set; }

        public override string ToString()
        {
            return this.Type == null ? string.Empty : this.Type.Name;
        }
    }
}
